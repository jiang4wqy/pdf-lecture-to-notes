"""
Convert the Obsidian-style markdown notes (produced by this skill) into Word
(.docx) using pandoc.

The note-generation step always writes a single source of truth: Obsidian-flavored
markdown (`[[wiki-links]]`, `![[embeds]]`, `> [!callouts]`). This script normalizes
that flavor into standard markdown that pandoc understands, then renders .docx.

Two modes:

    combined      One .docx for the whole course: 00 overview -> 01..0N main notes
                  -> example files (as an appendix), each separated by a page break.
                  A clickable table of contents is generated (--toc).

    per-lecture   One .docx per main note (NN_xxx.md). The paired example file
                  (例题与考点/NN_xxx_*.md) is folded in as an appendix of that file.

Usage:

    python build_docx.py --src "F:/我的笔记/.../corporate-finance" \
                         --mode combined \
                         --out  "F:/我的笔记/.../复习册.docx"

    python build_docx.py --src "F:/我的笔记/.../corporate-finance" \
                         --mode per-lecture \
                         --out  "F:/我的笔记/.../word"          # output DIRECTORY

Optional:

    --reference reference.docx   Style template (fonts/headings/margins). Generate
                                 an editable one with:
                                 pandoc -o reference.docx --print-default-data-file reference.docx
    --resource-path "F:/我的笔记" Where pandoc looks up images. Image paths in the
                                 notes are vault-root-relative (附件/图片/...), so this
                                 must point at the vault root. Default: parent of --src.
    --dry-run                    Print what would happen, write nothing.

Dependencies:
    pandoc (NOT a pip package) -- https://pandoc.org/installing.html
        Windows:  winget install --id JohnMacFarlane.Pandoc
        macOS:    brew install pandoc
        Linux:    sudo apt install pandoc

Exit codes:
    0   all OK
    1   missing dependency (pandoc)
    2   bad arguments / no notes found
    3   one or more pandoc conversions failed
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Obsidian callout type -> Chinese bold label used in the Word output.
CALLOUT_LABELS = {
    "info": "信息",
    "warning": "注意",
    "danger": "警告",
    "error": "警告",
    "note": "补充",
    "tip": "提示",
    "success": "重点",
    "important": "重点",
    "example": "例",
    "quote": "引用",
}

# Pandoc raw-OpenXML page break (works for docx output).
PAGE_BREAK = '```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n'

EXAMPLES_DIRNAMES = ("例题与考点", "Examples_and_Exam")


def normalize(md: str) -> str:
    """Turn Obsidian-flavored markdown into pandoc-friendly standard markdown."""
    # ![[path|alt]] / ![[path]]  ->  ![](path)   (image / file embed)
    md = re.sub(r"!\[\[([^\]\|]+?)(?:\|[^\]]*)?\]\]", r"![](\1)", md)

    # [[target|display]] -> display ; [[target]] -> last path segment (no extension)
    def _wikilink(m: str) -> str:
        inner = m.group(1)
        if "|" in inner:
            return inner.split("|", 1)[1]
        target = inner.split("#", 1)[0]          # drop heading anchor
        leaf = target.rsplit("/", 1)[-1]         # drop folder path
        return re.sub(r"\.md$", "", leaf)
    md = re.sub(r"\[\[([^\]]+?)\]\]", _wikilink, md)

    # > [!type] Title  ->  > **【Label】Title**   (only the marker line)
    def _callout(m: str) -> str:
        ctype = m.group(1).lower()
        title = m.group(2).strip()
        label = CALLOUT_LABELS.get(ctype, ctype)
        head = f"【{label}】{title}" if title else f"【{label}】"
        return f"> **{head}**"
    md = re.sub(r"^>\s*\[!([A-Za-z]+)\][-+]?\s*(.*)$", _callout, md, flags=re.MULTILINE)

    return md


def numeric_key(p: Path):
    """Sort key: leading zero-padded number prefix, else name. 00 < 01 < ... < 99."""
    m = re.match(r"(\d+)", p.stem)
    return (0, int(m.group(1)), p.name) if m else (1, 0, p.name)


def find_examples_dir(src: Path):
    for name in EXAMPLES_DIRNAMES:
        d = src / name
        if d.is_dir():
            return d
    return None


def main_notes(src: Path):
    """Top-level NN_*.md, numerically sorted, excluding the 00 overview."""
    notes = [p for p in src.glob("*.md") if re.match(r"\d", p.stem)]
    notes = [p for p in notes if not p.stem.startswith("00")]
    return sorted(notes, key=numeric_key)


def overview_note(src: Path):
    for p in src.glob("*.md"):
        if p.stem.startswith("00"):
            return p
    return None


def example_for(note: Path, ex_dir: Path):
    """Find the example file paired with a main note by matching the number prefix."""
    if ex_dir is None:
        return None
    m = re.match(r"(\d+)", note.stem)
    if not m:
        return None
    prefix = m.group(1)
    for p in sorted(ex_dir.glob("*.md"), key=numeric_key):
        if p.stem.startswith(prefix):
            return p
    return None


def run_pandoc(content: str, out_path: Path, resource_path: str, tmp_dir: Path,
               reference: Path, dry_run: bool) -> bool:
    """Write `content` to a temp .md and render it to out_path via pandoc.

    `resource_path` is a pandoc resource-path string (may list several roots
    separated by os.pathsep) so images resolve regardless of layout — both the
    course-local `images/...` scheme and the vault-root `附件/图片/...` scheme.
    """
    cmd = [
        "pandoc", "-f", "markdown", "-t", "docx",
        "--toc", "--toc-depth=2",
        f"--resource-path={resource_path}",
        "-o", str(out_path),
    ]
    if reference:
        cmd.append(f"--reference-doc={reference}")

    if dry_run:
        print(f"  would write {out_path}  ({len(content.splitlines())} md lines)")
        print(f"    cmd: {' '.join(cmd)} <tmp.md>")
        return True

    out_path.parent.mkdir(parents=True, exist_ok=True)
    # Temp file lives next to the source notes so course-local image paths
    # (images/...) still resolve; --resource-path covers the vault-root scheme.
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8",
                                     dir=str(tmp_dir), delete=False) as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)
    try:
        result = subprocess.run(cmd + [str(tmp_path)], capture_output=True, text=True)
    finally:
        tmp_path.unlink(missing_ok=True)

    if result.returncode != 0:
        print(f"  FAIL {out_path.name}: {result.stderr.strip()}", file=sys.stderr)
        return False
    print(f"  OK   {out_path}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--src", required=True, help="Folder of generated .md notes")
    parser.add_argument("--mode", required=True, choices=["combined", "per-lecture"])
    parser.add_argument("--out", required=True,
                        help="combined: output .docx file; per-lecture: output directory")
    parser.add_argument("--reference", help="Optional reference.docx style template")
    parser.add_argument("--resource-path",
                        help="Image lookup root(s) for pandoc, os.pathsep-separated. "
                             "Default: --src plus its parent dirs, covering both the "
                             "course-local images/... and vault-root 附件/图片/... schemes.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if shutil.which("pandoc") is None:
        print(
            "ERROR: pandoc not found on PATH. Install it (not a pip package):\n"
            "  Windows:  winget install --id JohnMacFarlane.Pandoc\n"
            "  macOS:    brew install pandoc\n"
            "  Linux:    sudo apt install pandoc\n"
            "See https://pandoc.org/installing.html",
            file=sys.stderr,
        )
        return 1

    src = Path(args.src)
    if not src.is_dir():
        print(f"ERROR: --src is not a directory: {src}", file=sys.stderr)
        return 2

    # Build the pandoc resource-path. Always include the course folder and its
    # parents (covers course-local images/... and vault-root 附件/图片/... schemes);
    # any user-supplied roots are searched first. Belt-and-suspenders so images
    # never silently drop just because the wrong single base was passed.
    roots = []
    if args.resource_path:
        roots.extend(args.resource_path.split(os.pathsep))
    roots.extend([str(src), str(src.parent), str(src.parent.parent)])
    seen, uniq = set(), []
    for r in roots:
        if r and r not in seen and Path(r).is_dir():
            seen.add(r)
            uniq.append(r)
    resource_path = os.pathsep.join(uniq)
    reference = Path(args.reference) if args.reference else None
    if reference and not reference.exists():
        print(f"ERROR: --reference not found: {reference}", file=sys.stderr)
        return 2

    ex_dir = find_examples_dir(src)
    notes = main_notes(src)
    overview = overview_note(src)

    if not notes and not overview:
        print(f"ERROR: no .md notes found in {src}", file=sys.stderr)
        return 2

    failures = 0

    if args.mode == "combined":
        parts = []
        ordered = ([overview] if overview else []) + notes
        if ex_dir:
            ex_files = sorted(ex_dir.glob("*.md"), key=numeric_key)
            if ex_files:
                ordered.append(None)  # marker -> appendix heading
                ordered.extend(ex_files)

        for item in ordered:
            if item is None:
                parts.append("# 附录：例题与考点\n")
                continue
            parts.append(normalize(item.read_text(encoding="utf-8")))

        content = ("\n\n" + PAGE_BREAK + "\n").join(parts)
        ok = run_pandoc(content, Path(args.out), resource_path, src, reference, args.dry_run)
        failures += 0 if ok else 1

    else:  # per-lecture
        out_dir = Path(args.out)
        for note in notes:
            parts = [normalize(note.read_text(encoding="utf-8"))]
            paired = example_for(note, ex_dir)
            if paired:
                parts.append("# 附录：本课例题与考点\n")
                parts.append(normalize(paired.read_text(encoding="utf-8")))
            content = ("\n\n" + PAGE_BREAK + "\n").join(parts)
            out_path = out_dir / f"{note.stem}.docx"
            ok = run_pandoc(content, out_path, resource_path, src, reference, args.dry_run)
            failures += 0 if ok else 1

    if failures:
        print(f"\nDone with {failures} failure(s).", file=sys.stderr)
        return 3
    print("\nAll conversions OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

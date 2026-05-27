"""
Extract specified pages from PDFs as PNG images using PyMuPDF (fitz).

The skill calling this script is responsible for picking which pages are worth
extracting. This script just renders + saves them at consistent quality.

Spec JSON shape (passed via --spec or stdin):

    [
        {
            "pdf": "Blockchain1.pdf",           # filename, resolved against --src
            "page": 5,                           # 1-indexed
            "subdir": "blockchain",              # under --dst
            "out_name": "cia_triad.png"         # final file name
        },
        ...
    ]

Usage:

    python extract_pdf_pages.py \
        --spec spec.json \
        --src  "C:/path/to/lecture/pdfs" \
        --dst  "F:/notes/attachments/images/course"

Optional:

    --zoom 2.0       # 1.0 = ~72 DPI, 2.0 = ~144 DPI (default), 3.0 = ~216 DPI
    --dry-run        # print what would be done, don't write files

Dependencies:
    pip install pymupdf

Exit codes:
    0   all OK
    1   missing dependency
    2   bad spec / arguments
    3   one or more pages failed (other pages may have succeeded)
"""

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--spec", required=True, help="Path to spec.json (see docstring)")
    parser.add_argument("--src", required=True, help="Directory containing the source PDFs")
    parser.add_argument("--dst", required=True, help="Destination directory for the PNG output")
    parser.add_argument("--zoom", type=float, default=2.0, help="Render zoom (default 2.0 ≈ 144 DPI)")
    parser.add_argument("--dry-run", action="store_true", help="Don't write files, just print")
    args = parser.parse_args()

    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("ERROR: PyMuPDF not installed. Run:  pip install pymupdf", file=sys.stderr)
        return 1

    src = Path(args.src)
    dst = Path(args.dst)
    spec_path = Path(args.spec)

    if not spec_path.exists():
        print(f"ERROR: spec file not found: {spec_path}", file=sys.stderr)
        return 2

    try:
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: spec is not valid JSON: {e}", file=sys.stderr)
        return 2

    if not isinstance(spec, list):
        print("ERROR: spec must be a JSON array", file=sys.stderr)
        return 2

    mat = fitz.Matrix(args.zoom, args.zoom)

    succeeded = 0
    failed = 0
    skipped_missing_pdf = 0
    skipped_oob_page = 0

    for i, entry in enumerate(spec, start=1):
        try:
            pdf_name = entry["pdf"]
            page_num = int(entry["page"])
            subdir = entry.get("subdir", "")
            out_name = entry["out_name"]
        except (KeyError, ValueError) as e:
            print(f"  [{i}] BAD ENTRY: {e}", file=sys.stderr)
            failed += 1
            continue

        pdf_path = src / pdf_name
        out_dir = dst / subdir if subdir else dst
        out_path = out_dir / out_name

        if not pdf_path.exists():
            print(f"  [{i}] SKIP (missing PDF): {pdf_path}", file=sys.stderr)
            skipped_missing_pdf += 1
            continue

        if args.dry_run:
            print(f"  [{i}] would render {pdf_name} p.{page_num} -> {out_path}")
            continue

        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            print(f"  [{i}] FAIL (cannot open {pdf_path}): {e}", file=sys.stderr)
            failed += 1
            continue

        try:
            if page_num < 1 or page_num > len(doc):
                print(f"  [{i}] SKIP (page {page_num} out of bounds, doc has {len(doc)}): {pdf_name}", file=sys.stderr)
                skipped_oob_page += 1
                continue

            out_dir.mkdir(parents=True, exist_ok=True)
            page = doc.load_page(page_num - 1)
            pix = page.get_pixmap(matrix=mat)
            pix.save(out_path)
            print(f"  [{i}] OK  {pdf_name} p.{page_num} -> {out_path}")
            succeeded += 1
        except Exception as e:
            print(f"  [{i}] FAIL ({pdf_name} p.{page_num}): {e}", file=sys.stderr)
            failed += 1
        finally:
            doc.close()

    total = len(spec)
    print(
        f"\nDone. {succeeded}/{total} succeeded, "
        f"{failed} failed, "
        f"{skipped_missing_pdf} skipped (missing PDF), "
        f"{skipped_oob_page} skipped (page out of bounds)."
    )

    if failed > 0:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())

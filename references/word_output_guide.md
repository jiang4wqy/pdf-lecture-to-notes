# Word (.docx) Output Guide

How the Word branch works. The note-generation step is **format-agnostic** — it
always writes the same Obsidian-flavored markdown. This guide covers the last
mile: turning that markdown into Word via `scripts/build_docx.py` (a pandoc wrapper).

> 单一内容源原则：**不要为 Word 单独写一套笔记**。永远只生成一次 Obsidian markdown，
> Word 由脚本转换。这样模板只维护一处。

---

## Prerequisite: pandoc

`build_docx.py` shells out to **pandoc** (not a pip package):

```powershell
winget install --id JohnMacFarlane.Pandoc   # Windows
brew install pandoc                          # macOS
sudo apt install pandoc                       # Linux
```

The script checks for pandoc on PATH and prints this hint if missing (exit code 1).
If the user can't / won't install pandoc, fall back to delivering the Obsidian
markdown only and tell them.

---

## The two granularities

| Mode | Command flag | Produces |
|---|---|---|
| 整门课一份 | `--mode combined` | One `.docx`: 封面/TOC → `00_总览` → `01..0N` 主笔记 → `99_综合模拟卷` → 附录(所有例题)，文件间分页。`--out` 是一个 `.docx` 文件路径。 |
| 一课一份 | `--mode per-lecture` | 每份主笔记一个 `.docx`，配套例题作为附录折叠进去。`--out` 是一个**目录**。 |

```bash
# 整门课一份
python scripts/build_docx.py --src "F:/我的笔记/.../corporate-finance" \
    --mode combined --out "F:/我的笔记/.../corporate-finance/复习册.docx"

# 一课一份
python scripts/build_docx.py --src "F:/我的笔记/.../corporate-finance" \
    --mode per-lecture --out "F:/我的笔记/.../corporate-finance/word"
```

The script auto-discovers `00_*.md` (overview), `NN_*.md` (main notes, numerically
ordered, `99` mock exam last), and the `例题与考点/` (or `Examples_and_Exam/`)
sub-folder, pairing each example file to its main note by number prefix.

---

## Markdown → Word syntax conversion (handled automatically)

`build_docx.py` normalizes Obsidian flavor before calling pandoc:

| Obsidian markdown | Becomes in Word | Mechanism |
|---|---|---|
| `![[附件/图片/x.png]]` / `![[x.png\|alt]]` | inline image | regex → `![](x.png)`, pandoc embeds it |
| `[[note]]` / `[[note#heading\|显示名]]` | plain text (`显示名` or leaf name) | regex strips brackets (Word has no backlinks) |
| `> [!info] 考试地位` | `> **【信息】考试地位**` | callout marker → bold Chinese label, body stays as a quote |
| `$x$` / `$$...$$` | **native Word equation (OMML)** | pandoc, out of the box ✅ |
| pipe tables | native Word tables | pandoc ✅ |
| `# 标题` levels | Word heading styles + TOC entries | pandoc `--toc` ✅ |

Callout label map (`build_docx.py` → `CALLOUT_LABELS`): info→信息, warning→注意,
danger/error→警告, note→补充, tip→提示, success/important→重点, example→例, quote→引用.
Unknown types keep their raw name. Edit that dict to change labels.

---

## Image resolution — the one thing to get right

Image embeds are **relative**, and the base differs by how the notebook was built:

- vault-root scheme: `![[附件/图片/<course>/x.png]]` → base is the **vault root**
- course-local scheme: `![[images/ch01/x.png]]` → base is the **course folder**

pandoc finds images via `--resource-path`. `build_docx.py` **always** searches
`--src` plus its parent dirs (os.pathsep-joined), which covers both schemes. Any
`--resource-path` you pass is **added in front** (searched first) — it never
replaces the defaults, so images can't silently drop from passing the wrong base.
If a course sits deep in the vault (`vault/学习/database/`) and uses the
`附件/图片/...` scheme, you can still pass the vault root explicitly for clarity:

```bash
... --resource-path "F:/我的笔记/123"
```

When the skill itself invokes this script, it already knows the image base from
the extraction step — pass it as `--resource-path` to be safe. Multiple roots can
be joined with `;` (Windows) / `:` (macOS/Linux).

If an image still doesn't resolve, pandoc just omits it (no hard failure) — verify
the media count after conversion (see below).

---

## Styling: optional reference.docx

By default the .docx uses pandoc's built-in styles. To customize fonts, heading
colors, margins, generate an **editable** style template once and pass it:

```bash
pandoc -o reference.docx --print-default-data-file reference.docx
# open reference.docx, restyle the named styles (Heading 1, Body Text, ...), save
python scripts/build_docx.py ... --reference reference.docx
```

Keep a tuned `reference.docx` in the course folder (or skill root) for a consistent
house style across exports.

---

## Verify the .docx (quick checks)

After conversion, sanity-check by unzipping the docx (it's a zip):

```python
import zipfile
d = zipfile.ZipFile(r"C:\path\复习册.docx").read("word/document.xml").decode("utf-8", "ignore")
print("images:", len([n for n in zipfile.ZipFile(r"C:\path\复习册.docx").namelist() if n.startswith("word/media/")]))
print("OMML equations:", d.count("<m:oMath"))   # >0 if the course has LaTeX
print("residue [[ :", d.count("[["), " ![[ :", d.count("!["[:3]))  # must be 0
print("TOC present:", "instrText" in d)
```

Expect: images > 0 (if any were extracted), `[[` / `![[` residue == 0, TOC present,
and OMML > 0 for any course with formulas.

---

## When NOT to use Word

- The user lives in Obsidian and wants backlinks / graph view → Word loses those;
  keep Obsidian.
- Heavy interactive cross-referencing → Word's flat structure is worse.

Word shines for: printing, emailing a single 复习册 to classmates, submitting as a
deliverable, or readers who don't use Obsidian.

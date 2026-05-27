---
name: pdf-lecture-to-obsidian
description: |
  Build a complete Obsidian-style study notebook from a folder of lecture PDFs (or a single PDF). The user supplies an input folder (lecture slides, exam reviews, practice papers) and an output folder; this skill produces a structured set of linked .md notes — one main note per lecture, an index/overview, an "examples & exam questions" sub-folder with bidirectional `[[wiki-links]]`, and key page images extracted to a sibling attachments folder. Use whenever the user wants to: "整理 PDF 笔记", "把课件做成笔记", "make Obsidian notes from these slides", "build a study notebook", "为我做笔记", "课程复习笔记", "把这些 lecture 做成笔记", "PDF to markdown notes for studying", or supplies a folder full of lecture PDFs and wants organized notes. Trigger even if the user just says "笔记" + mentions a folder of PDFs/slides — they almost certainly want this workflow rather than a single-file conversion.
---

# PDF Lectures → Obsidian Study Notebook

> Turn a folder of lecture PDFs into a structured, linked, exam-ready notebook in the user's Obsidian-style vault.

## What this skill produces

Given an input folder of lecture PDFs and an output folder, produce:

1. **One main note per lecture** (`01_xxx.md`, `02_xxx.md`, ...) — covers all key concepts with definitions, formulas, worked numerical examples, comparison tables, common pitfalls, and a "must-know cheat sheet" section at the end. Important English terms preserved (key sentences and proper nouns); explanations in the user's working language (Chinese by default for Chinese-named folders, otherwise English).
2. **`00_总览.md` / `00_Overview.md`** — index file, exam-relevance mapping, suggested study order.
3. **`例题与考点/` sub-folder** (or `Examples_and_Exam/`) — one file per main note with: concept distinctions, worked problems, short-answer questions, applied problems, and an exam checklist. Linked **bidirectionally** to main notes via `[[wiki-links]]`.
4. **Extracted PNG images** of key pages (formulas, flowcharts, diagrams, tables) saved to a sibling `附件/图片/<course-name>/` (or `attachments/images/<course-name>/`) folder, organized by topic. Embedded into notes via Obsidian's `![[...]]` syntax.
5. **Optional: comprehensive mock exam paper** (`99_综合模拟卷.md`) — integrates any practice/review PDFs found in the input folder; all questions linked back to relevant main notes.

## Inputs the user must provide

- **Input folder** — contains the lecture PDFs. May also contain a review/syllabus PDF and a practice exam PDF (auto-detect by filename keywords like `review`, `practice`, `final`, `复习`, `期末`, `模拟`).
- **Output folder** — where notes go. Conventionally `F:\我的笔记\<vault>\<course>\` or similar. Sub-folder `例题与考点/` is created here.
- **Attachments folder** — where images go. Default: a sibling folder like `<vault-root>\附件\图片\<course>\`. Ask if unclear.

If any are missing, ask for them up front in one batch (don't ask one at a time).

## Default decisions baked into this skill

These were chosen by the user when the skill was created. Override only if the user explicitly asks for something different.

| Decision | Default |
|---|---|
| Output format | **Obsidian wiki-link style** — `[[file]]`, `![[image.png]]`, callouts `>[!info]`, `>[!warning]`, math `$...$` / `$$...$$` |
| Image extraction | **Smart page selection** — scan the PDF, pick pages with formulas/diagrams/flowcharts/comparison tables; render at zoom=2.0 (≈144 DPI) PNG via PyMuPDF |
| `例题与考点/` sub-folder | **Ask at runtime** — propose generating it; if user agrees, produce one example file per main note plus a mock-exam file if a practice PDF exists |
| Language | Match the input/output path naming. Chinese path components → Chinese explanations + English key terms. English path → all English. |
| Note size | ~400–600 lines per main note (medium detail). |

## High-level workflow

Follow these steps in order. Don't skip the planning step — it prevents wasted work when the user's vault has surprises.

### Step 1 — Discover

1. List all PDFs in the input folder. Use the Read tool with the PDF paths (Claude can read PDFs natively) — do NOT extract text manually unless PyMuPDF is unavailable.
2. Identify special files by filename keywords:
   - `review` / `复习` / `summary` / `outline` → exam outline / syllabus (read first to learn what's important)
   - `practice` / `模拟` / `mock` / `sample` → practice exam (target for `99_综合模拟卷.md`)
   - `assignment` / `hw` / `作业` → assignment template; not always note-worthy, ask user
   - Numbered or dated lectures (`Week 1.pdf`, `Lecture 4 - X.pdf`, `1 Intro.pdf`) → main lecture material
3. Briefly read the review/syllabus PDF (if any) to extract: the official module list, key topics to emphasize, types of exam questions. This **drives the structure** of the notebook.

### Step 2 — Plan and confirm

Present the user with a concrete plan before writing anything:

- Proposed list of main notes (one per lecture or per module, mapped to PDFs)
- Proposed sub-folder for examples
- Proposed image attachments folder path
- Whether to generate the mock-exam file (`99_综合模拟卷.md`)
- Approximate output volume (file count + line count estimate)

Wait for the user to confirm or adjust before extracting images or writing files. If they want changes, revise the plan.

### Step 3 — Extract images

Run `scripts/extract_pdf_pages.py` (see below) to render selected PDF pages as PNG.

If PyMuPDF is unavailable on the user's system, fall back to: skip image extraction, use Mermaid for flowcharts and ASCII tables for matrices. Tell the user so they're not surprised.

### Step 4 — Write the notes

Use the templates in `references/`:

- `references/main_note_template.md` — every main lecture note
- `references/example_template.md` — every file in `例题与考点/`
- `references/overview_template.md` — the `00_总览.md`
- `references/mock_exam_template.md` — `99_综合模拟卷.md`

These templates are scaffolds, not rigid forms. Adapt section headings to the lecture's actual content. Always include:
- A `> [!info] 考试地位` callout at the top mapping to the review/syllabus
- A "公式速记表" at the end
- A "易错点" section
- Cross-links to related notes via `[[]]`

### Step 5 — Cross-link

After all main notes exist, go back and add `[[other_note]]` links inline wherever one lecture's concepts are used in another. Also link main notes ↔ example files in both directions (Obsidian renders backlinks automatically, but explicit links help).

### Step 6 — Verify

1. List final files and image count
2. Confirm at least one main note has an image embedded via `![[...]]`
3. Confirm at least one main note links to its example file via `[[例题与考点/...]]`
4. Confirm `00_总览.md` indexes every main note
5. Report to the user with: total file count, total line count, image count, paths to inspect

## When to use `scripts/extract_pdf_pages.py`

This script is the core image-extraction tool. **Always prefer it over hand-rolled image extraction** — it handles edge cases (encoded glyphs, missing pages, non-existent PDFs) and outputs at consistent resolution.

Usage:

```bash
python scripts/extract_pdf_pages.py --spec <path-to-spec.json> --src <input-folder> --dst <output-image-folder>
```

The `spec.json` shape is documented in the script's docstring. Generate it programmatically based on the PDFs you've read — Claude picks the relevant page numbers based on what was on each page (formulas, flowcharts, comparison tables, key diagrams).

If you need to render a quick one-off page outside the structured spec, you can run a small inline Python snippet using PyMuPDF directly — the script is just a convenience for batch jobs.

## Common pitfalls (avoid these)

- **Don't extract every page.** A 50-slide PDF doesn't need 50 PNGs. Pick 3–8 pages per PDF — the ones a student would actually want to look at while reviewing.
- **Don't write the main notes before reading the review/syllabus PDF.** The review tells you what to emphasize; without it you'll produce a generic dump.
- **Don't translate proper nouns or formulas.** "Bellman equation", "Sharpe Ratio", "Q-Learning", "SHA-256" stay in English. Chinese is for the surrounding explanation.
- **Don't make every note the same length.** A foundational module deserves more lines than a peripheral one.
- **Don't fabricate exam questions** — use only what's actually in the practice/review PDFs, plus clearly-labeled derived/generated practice questions for concepts that lack official examples.
- **Don't create `小组作业/`, `assignment/`, etc.** — these are the user's working areas, leave them alone.

## Important nuances

### Bidirectional linking

Every main note must have a `## 🔗 相关链接` section with at least:
- `[[例题与考点/0X_xxx_例题与考点]]`
- `[[00_总览]]`
- Cross-references to other lectures where concepts overlap

Every example file must have a `## 🔗 反向链接` section linking back to:
- The corresponding main note
- The overview
- The mock exam (if present)
- Any sibling example files that share concepts

### Image embedding paths

Obsidian resolves `![[image.png]]` against the vault root. So if the vault is `F:\我的笔记\` and images are at `F:\我的笔记\附件\图片\<course>\xxx.png`, the embed should be:

```markdown
![[附件/图片/<course>/xxx.png]]
```

Or (if the user prefers shorter paths) configure Obsidian to search subfolders and just use `![[xxx.png]]`. Default to the explicit relative path from vault root — it's more robust.

### Path with spaces and Chinese characters

Always quote paths in shell commands. Use forward slashes `/` in scripts and `\\` in Windows shell calls. When in doubt, prefer the Read/Write/Glob tools over shell commands for file paths with non-ASCII characters.

### Existing files

If the output folder already has notes, **ask before overwriting**. Common case: the user is re-running on the same course and wants to refresh. Default behavior: rename old files to `<name>.bak.md` then write new ones.

## Quick-start checklist

When invoked, work through this list:

1. ☐ Read the input-folder listing
2. ☐ Identify review/practice/lecture PDFs
3. ☐ Read the review PDF (if present) to learn structure
4. ☐ Skim each lecture PDF (read first + middle + last few pages to get scope)
5. ☐ Present plan; await user confirmation
6. ☐ Run image extraction
7. ☐ Write main notes (one at a time; use templates)
8. ☐ Ask user if they want `例题与考点/` sub-folder
9. ☐ Write example files (if requested)
10. ☐ Write mock exam (if practice PDF exists and user wants it)
11. ☐ Write `00_总览.md` last (links all the above)
12. ☐ Verify file count, image count, link integrity
13. ☐ Report to user with paths and stats

## Tone in produced notes

- Direct and exam-oriented. Not academic prose.
- Use callouts for emphasis: `> [!warning] 易错点 ⭐⭐⭐`
- Use tables for comparisons (always preferable to long bulleted distinctions)
- Use math display equations (`$$...$$`) for key formulas
- Mark exam-relevance with ⭐ ratings (⭐⭐⭐ = certain to be on the exam; ⭐ = nice to know)
- Always end with a "must-memorize" cheat-sheet table

## Reference files in this skill

- `references/main_note_template.md` — main lecture note scaffold
- `references/example_template.md` — example/exam-question file scaffold
- `references/overview_template.md` — `00_总览.md` scaffold
- `references/mock_exam_template.md` — comprehensive mock exam scaffold
- `references/workflow_checklist.md` — step-by-step checklist (handy mid-task)

Read these on demand as you need them; don't try to memorize them all upfront.

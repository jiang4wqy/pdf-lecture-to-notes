# Workflow Checklist

Mid-task reference. When you're deep in writing notes, pull this up to make
sure you haven't skipped a step.

Structure: **Part A (Phases A–H)** is format-agnostic and always runs — it
produces the Obsidian-flavored markdown source of truth. **Part B** is one of
two branches depending on the output target chosen in Phase B.

---

# PART A — Format-agnostic core

## Phase A — Discover (~10 min)

- [ ] List all PDFs in input folder via Glob
- [ ] Identify special PDFs by name keywords:
  - `review` / `复习` / `summary` / `outline` → syllabus
  - `practice` / `模拟` / `sample` / `mock` → mock exam source
  - `assignment` / `作业` → optional; check with user
- [ ] Read the syllabus/review PDF in full (it determines structure)
- [ ] For each lecture PDF, skim first 3 pages + last 3 pages to gauge scope

## Phase B — Plan (~5 min, then USER CONFIRMATION)

- [ ] Map each lecture PDF to one main note title
- [ ] Decide which lectures (if any) should be merged or split
- [ ] Identify what images deserve extracting (target ~3–8 per PDF)
- [ ] Confirm output paths (main folder + example sub-folder + image folder)
- [ ] **Ask output target: Obsidian (default) / Word-combined / Word-per-lecture**
      → decides which Part B branch to run later
- [ ] Present plan to user, wait for confirmation

## Phase C — Extract images (~5 min)

- [ ] Generate `spec.json` listing all (pdf, page, subdir, name) tuples
- [ ] Run `scripts/extract_pdf_pages.py --spec ... --src ... --dst ...`
- [ ] Verify image count = expected (script reports it)
- [ ] If PyMuPDF missing, fall back to Mermaid / ASCII

## Phase D — Write notes (the bulk of the work)

For each lecture PDF:
- [ ] Read template `references/main_note_template.md` (once is enough)
- [ ] Read the PDF carefully (every page if < 50 pages; otherwise focus on
      headings + boxed formulas + summaries)
- [ ] Write the main note:
  - [ ] `> [!info] 考试地位` callout at top mapping to review
  - [ ] Outline
  - [ ] Body sections, English terms in bold, formulas in LaTeX
  - [ ] Embedded images via `![[...]]`
  - [ ] Comparison tables for "vs" content
  - [ ] Numerical examples with step-by-step
  - [ ] ⭐ star markers on exam-relevant material
  - [ ] **公式速记表** at the end
  - [ ] **易错点** section
  - [ ] **相关链接** section at the very end

## Phase E — Example files (if user opted in)

For each main note:
- [ ] Read template `references/example_template.md`
- [ ] Write the paired example file:
  - [ ] 易混淆辨析 (first; it's the meat of the file)
  - [ ] 典型计算题 with step-by-step
  - [ ] 概念短答
  - [ ] 综合应用
  - [ ] 必背清单
  - [ ] **反向链接** section

## Phase F — Mock exam (only if practice PDF exists)

- [ ] Read template `references/mock_exam_template.md`
- [ ] Transcribe every question from the practice PDF
- [ ] Give each question an answer block (`<details>` with link to main note)
- [ ] Add the MCQ answer-key table
- [ ] Add high-frequency topic summary

## Phase G — Overview (LAST)

- [ ] Read template `references/overview_template.md`
- [ ] Write `00_总览.md`:
  - [ ] Module index table with links to all main notes + example files
  - [ ] Necessary cheat sheet
  - [ ] Study path (Mermaid OK)
  - [ ] Image folder layout

## Phase H — Cross-link sweep

(Do this for both targets — it improves the markdown even though Word drops backlinks.)

- [ ] Open every main note; scan for places where another lecture's
      concept appears and add `[[link]]`
- [ ] Verify every main note links to its example file
- [ ] Verify every example file links back to its main note
- [ ] Verify overview file links to everything

---

# PART B — Format-specific output (run ONE branch)

## Branch Obsidian — Phase I: Verify and report

- [ ] Count main notes, example files, images
- [ ] Confirm at least one `![[...]]` per main note (where appropriate)
- [ ] Confirm overview indexes every main note
- [ ] Report to user with paths, counts, and what to open first

## Branch Word — Phase W1: Build .docx

- [ ] Confirm pandoc is installed (`pandoc --version`); if not, print install
      hint or fall back to delivering the `.md` only
- [ ] Run `scripts/build_docx.py` with `--mode combined` or `--mode per-lecture`
- [ ] Pass `--resource-path <vault-root>` so images resolve
- [ ] (Optional) pass `--reference reference.docx` for custom styling

## Branch Word — Phase W2: Verify and report

- [ ] Confirm `.docx` file(s) written with non-trivial size
- [ ] Unzip-check one: images in `word/media/`, no `[[`/`![[` residue, TOC
      present, formulas as native equations (math courses)
- [ ] Report to user with output path(s), size, and note that `.md` source is kept

---

## Quick stats for a typical course (calibration)

- 5–8 main notes
- 5–8 example files (one per main note)
- 1 overview file
- 1 mock exam (if practice PDF exists)
- 15–30 images
- Total ~3000–6000 lines of markdown

A small course (4 lectures, no review/practice) might be:
- 4 main notes
- (no example files, if user declined)
- 1 overview
- ~10 images
- ~1500 lines

Big course (10 lectures + heavy review):
- 10 main notes
- 10 example files
- 1 overview
- 1 mock exam
- ~40 images
- ~8000 lines

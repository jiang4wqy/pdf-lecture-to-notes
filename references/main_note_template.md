# Main Lecture Note Template

This is the scaffold for `0N_<lecture-title>.md`. Read it, then adapt section
headings to whatever the lecture actually covers. Don't blindly copy structure
that doesn't fit.

---

## Frontmatter and intro

```markdown
# Module N - <English Lecture Title>

> [!info] 考试地位
> 在 <review/syllabus PDF 名字> 中对应 Module X。**重点考点**：……（从 review PDF 直接摘）。

返回 [[00_总览]] · 配套例题 [[例题与考点/0N_xxx_例题与考点]]

---

## Outline
1. 第一节标题
2. 第二节标题
3. ...
```

The `> [!info]` callout at the top is mandatory. It maps this note to the
official syllabus / review PDF — that's how the user knows what to memorize
vs what's just context.

---

## Body sections

For each main concept, use this rhythm:

```markdown
## 1. <Section title>

### Definition / 定义
- **English term**: 中文解释
- 公式（LaTeX 行内 $x$ 或独立 $$X$$）

### Why / 为什么
中文写直觉、动机、上下文。**不要**只翻译英文 — 用学生听得懂的话解释为什么这个东西重要。

### Example / 例子
数值例子 step-by-step。

> [!warning] 易考点 ⭐⭐⭐
> 这里是 review 大纲明确点名的内容……

> [!note] 拓展（非考点）
> 这部分加深理解但不会考……
```

Star ratings:
- ⭐⭐⭐ — definitely on the exam (per review PDF)
- ⭐⭐ — likely (judgment call based on emphasis)
- ⭐ — nice to know

---

## Embedded images

Pull in the PNGs extracted by `scripts/extract_pdf_pages.py`. Use Obsidian's
embed syntax with the path **relative to the vault root**:

```markdown
![[附件/图片/<course-name>/<topic>/<image>.png]]
```

If you don't know the vault root, ask. Don't hardcode `F:\...` absolute paths.

---

## Tables for comparisons

Whenever the lecture compares two methods / generations / approaches, use a
table — much more digestible than prose. Always include a column showing
"what flaw does this fix / introduce".

```markdown
| Generation | Method | Solves | Still missing |
|---|---|---|---|
| 1 | BoW | numeric features | word order |
| 2 | TF-IDF | weighting | semantic relations |
| 3 | Word2Vec | semantic | context-dependence |
| 4 | BERT | full context | interpretability |
```

---

## Formula cheat sheet (mandatory at the end)

Every main note ends with:

```markdown
## 🔥 公式速记表（必背）

| 概念 | 公式 |
|------|------|
| Sharpe Ratio | $SR = \frac{R_p - R_f}{\sigma_p}$ |
| Max Drawdown | $MDD = \frac{V_{peak} - V_{trough}}{V_{peak}}$ |
| ... | ... |
```

This is the section the user re-reads on the night before the exam. It must
be comprehensive but skimmable.

---

## Common pitfalls section (mandatory)

```markdown
## ⚠️ 易错点

1. **Bullet that names the trap**：解释为什么容易错 + 怎么避免
2. ...
```

Aim for 5–10 items. Real pitfalls students actually fall into, not platitudes.

---

## Cross-link section (mandatory at the very end)

```markdown
## 🔗 相关链接

- 配套例题: [[例题与考点/0N_xxx_例题与考点]]
- 综合模拟: [[例题与考点/99_综合模拟卷]]
- 前置/相关: [[0M_other_note]]
- 返回总览: [[00_总览]]
```

If two main notes share a concept (e.g., Sharpe Ratio appears in both
"Evaluation Metrics" and "Risk Management"), make sure they explicitly
link each other. Obsidian's backlink panel will reflect this.

---

## Tone

- Direct, exam-oriented. Skip filler.
- Mix English (key terms, proper nouns, formulas) with Chinese (explanations).
- Use callouts liberally: `> [!info]`, `> [!warning]`, `> [!tip]`, `> [!note]`.
- LaTeX for all math. Don't write "alpha" — write `$\alpha$`.
- Bold the technical terms on first introduction: **Bellman equation**.

## Length target

- ~400–600 lines per main note (medium detail). Override if the lecture's
  intrinsic content is much smaller or larger.
- Smaller note OK for peripheral topics; bigger note OK for foundational
  ones (e.g., the lecture the syllabus singles out as central).

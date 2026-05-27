# Example / Exam-Questions File Template

Scaffold for files in `例题与考点/0N_xxx_例题与考点.md`.

The file serves three purposes:
1. **Disambiguate** concepts that students confuse (the "辨析" section)
2. **Worked numerical problems** with step-by-step solutions
3. **Conceptual short-answer drills** + applied problems

Every example file is **paired with one main note** via bidirectional links.

---

## Structure

```markdown
# Module N - <Title> 例题与考点

> 关联笔记: [[0N_主笔记]] · 返回 [[00_总览]]

---

## 一、易混淆概念辨析 ⚠️

### 1. <Concept A> vs <Concept B>

| | A | B |
|---|---|---|
| 定义 | ... | ... |
| 公式 | ... | ... |
| 何时用 | ... | ... |
| 易错 | ... | ... |

### 2. <Another distinction>
...

---

## 二、典型计算题

### Q1. <Topic> ⭐⭐⭐

**题**：题干（含数字）。

**Solution**：

Step 1 — ...
$$\text{公式}$$

Step 2 — ...

**答案：X**

> 回顾: [[0N_主笔记#相关章节]]

---

### Q2. ...

---

## 三、概念题（短答）

### Q5. <Question>?

**答**：……（2-4 句，精炼）。

### Q6. ...

---

## 四、综合应用题

### Q12. <Scenario-based problem> ⭐⭐⭐

**题**：场景描述。

**答**：
1. 步骤一
2. 步骤二
3. ...

---

## 五、Review 大纲映射题

> 这些题对应 review PDF 中明确点名的能力。

### Q15. ...

---

## 🎯 必背清单

- [ ] 公式 1
- [ ] 概念 2
- [ ] ...

---

## 🔗 反向链接

- 返回主笔记: [[0N_主笔记]]
- 综合模拟: [[例题与考点/99_综合模拟卷]]
- 相关：[[0M_其他笔记]]（如概念跨模块）
- 总览: [[00_总览]]
```

---

## Question-generation rules

1. **First** use any questions from the practice/review PDFs verbatim
   (or near-verbatim) — those are the highest-signal exam predictors.
2. **Second** generate derived questions: change numbers in textbook
   examples to test the same concept.
3. **Third** generate fresh conceptual questions — but only on
   topics that the syllabus / review marked as important.
4. **Don't fabricate** "real exam questions" — be honest about
   which are direct and which are derived/generated. You can label
   them with a small note: `> 来源：派生题` or similar.

## How many questions per file

- Min 6, target 12–18. More for exam-heavy modules.
- Mix difficulty: 30% easy (definition recall), 50% medium
  (compute / apply), 20% hard (multi-step / integration).

## Mandatory sections

Every example file needs:
- **易混淆辨析** at the start (this is where the file earns its keep)
- **必背清单** near the end (checklist for self-test)
- **反向链接** at the very end (Obsidian backlink hygiene)

# Mock Exam Template (`99_综合模拟卷.md`)

This file integrates any **practice exam PDF** found in the input folder.
It's optional — only produce it if such a file exists OR the user explicitly
asks for one.

---

## Structure

```markdown
# 综合模拟卷（基于 <practice-pdf-name>）

> [!info] 说明
> - 来源：`<practice-pdf-name>`
> - 共 N MCQ + M 短答 + K 大题
> - 全部题目附**参考答案**和**笔记链接**
> - 建议先**遮住答案做一遍**，再对照解析

返回 [[00_总览]]

---

## Part I: Multiple Choice (X 分)

### Q1.1 [Module - Topic]
题目正文。

(a) 选项 A
(b) 选项 B
(c) 选项 C
(d) 选项 D

<details>
<summary>答案</summary>

**(b)** — 简短解释为什么。
回顾: [[0N_主笔记#相关章节]]

</details>

---

### Q1.2 ...

---

### MCQ 答案速查

| Q | 答 | Q | 答 |
|---|---|---|---|
| 1.1 | b | 1.6 | a |
| ... | | ... | |

---

## Part II: Short Answer (X 分)

### Q2.1 [Module - Topic, X 分]
题目。

<details>
<summary>参考答案</summary>

要点：
- 点 1
- 点 2

回顾: [[0N_主笔记]]

</details>

---

## Part III: Essay / Applied Questions (X 分)

### Q3.1 [Topic, 10 分]
长题。

<details>
<summary>参考答案要点</summary>

**思路**：
1. 步骤
2. 步骤

**关键公式**：$...$

**注意**：常见陷阱说明

</details>

---

## Part IV: Bonus (optional)

### Q4.1
...

---

## 🎯 高频考点总结

按出现频率排序：

1. 考点 1 - 来自 Q1.1, Q2.3, Q3.2
2. 考点 2 - ...

---

## 📚 答题策略

| 题型 | 准备方法 |
|------|----------|
| MCQ | 反复背概念辨析 |
| Calc | 不看笔记练公式 |
| Concept | 精准术语 |
| Applied | 子题分块 |
| Essay | 图/公式/表 > 纯文字 |
| Time | 1 分钟/分 |

---

## 🔗 反向链接

- 总览: [[00_总览]]
- Module 1: [[例题与考点/01_xxx_例题与考点]]
- ...
```

---

## Sourcing rules

- Every MCQ option must come from the practice PDF or be a clear
  derivative. Don't make up plausible-sounding distractors out of
  thin air — they often turn out to be technically correct.
- For short-answer and essay questions, you can include both
  practice-PDF questions and Claude-generated ones, but label
  them clearly.
- For each question, the `<details>` block with the answer must
  link back to the relevant main note section via `[[]]#anchor`.

## Length

Whatever the practice PDF has, plus an answer-key table for MCQ and
a high-frequency-topic summary at the end. Typically 400–700 lines.

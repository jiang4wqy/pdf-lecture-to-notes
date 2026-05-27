# pdf-lecture-to-obsidian — 使用指南

> 你已经做出这个 skill 了，那么以后怎么用它？这份文档讲清楚。

---

## 一、Skill 在哪里？什么时候自动触发？

**位置**：`C:\Users\lenovo\.claude\skills\pdf-lecture-to-obsidian\`

Claude Code 启动时自动扫描 `~/.claude/skills/`，把所有 skill 注册到列表里。你打开 Claude Code 就能用，无需任何额外操作。

**自动触发场景**（基于 `SKILL.md` 中的 `description` 字段）：

| 你说的话 | 会触发 |
|----------|--------|
| "F:\我的笔记 下整理一下「机器学习」的 PDF 笔记" | ✅ |
| "把这堆 lecture 做成 Obsidian 笔记" | ✅ |
| "桌面那个课件文件夹做成笔记吧" | ✅ |
| "Build me study notes from this folder of PDFs" | ✅ |
| "PDF to Obsidian notes for my Stats course" | ✅ |
| "读一下 chapter5.pdf 第 7 页讲了什么" | ❌（不该触发 — 那是单 PDF 阅读）|
| "把 invoice.pdf 文字提取出来" | ❌ |
| "Merge these 3 PDFs into one" | ❌ |

如果该触发但没触发：手动调用 → 在对话里说"**用 pdf-lecture-to-obsidian skill**"。

---

## 二、典型使用流程（你将来要做的）

### 场景 A — 给一门新课做完整笔记

1. **进 Claude Code，开新会话**

2. **直接说要求**，例如：

   ```
   把 C:\Users\lenovo\OneDrive\Desktop\大三\金融概论\ 这门课做成
   Obsidian 笔记，放到 F:\我的笔记\123\大三笔记\corporate-finance\，
   图片放 F:\我的笔记\123\附件\图片\ 下。要主笔记 + 例题 + 总览。
   ```

3. **Claude 会做什么**（按 SKILL.md 中的工作流）：
   1. 列出输入文件夹下所有 PDF
   2. 识别 review / practice / lecture（按文件名关键词）
   3. 读 review PDF（如果有）→ 学到考试结构
   4. 给你**一个计划**：建议的笔记列表、文件名、要不要例题、要不要模拟卷
   5. **等你确认**
   6. 提取关键 PDF 页为 PNG（用 `scripts/extract_pdf_pages.py`）
   7. 写主笔记（按 `references/main_note_template.md` 的模板）
   8. 写例题文件（如果你同意）
   9. 写综合模拟卷（如果有 practice PDF）
   10. 最后写 `00_总览.md`
   11. 跨链接扫描
   12. 给你报告：文件数、行数、图片数、第一个该打开的文件

4. **预计时间**：4-8 份 PDF 约 30-60 分钟

---

### 场景 B — 只想快速搞一份 PDF

```
F:\我的笔记\123\附件\图片 下保存图片。
帮我把 "C:\path\to\lecture.pdf" 做成一份 Obsidian 笔记，
放 F:\我的笔记\quick\ 下。不要例题，不要总览，一份就行。
```

skill 会跳过例题 + 总览，只输出 1 份主笔记。

---

### 场景 C — 已经做过的课程要补充/重做

```
F:\我的笔记\123\大三笔记\fintech\ 我已经做过了，但
C:\path\to\fintech\ 下又加了 2 个新 PDF，麻烦补到笔记里。
```

skill 会：
- 检查已有文件，不直接覆盖（默认 rename 旧文件为 `.bak.md`）
- 新增主笔记
- 更新 `00_总览.md` 加入新条目
- 加交叉链接

---

## 三、Skill 的"配置"——你能改什么？

所有可改项都在 `SKILL.md` 里。常见的修改：

### 改默认输出风格
找到 `## Default decisions baked into this skill` 那张表，改对应行。例如：
- 想要纯 Markdown（不要 Obsidian wiki-link）→ 改 "Output format" 行
- 永远生成例题文件夹（不再问）→ 改 "例题与考点 sub-folder" 行为 "Always generate"

### 改图片提取的"智能选页"逻辑
不直接在 skill 里写规则，而是在 prompt 里加约束。例如：
```
要求每个 PDF 至少提取 8 张图，每张都要包含公式。
```

### 改默认笔记长度
SKILL.md 里 "Note size" 行从 "400-600" 改为你想要的。

---

## 四、依赖检查

Skill 需要本机有：

| 工具 | 用途 | 怎么检查 |
|------|------|---------|
| Python ≥ 3.8 | 跑 extract_pdf_pages.py | `python --version` |
| PyMuPDF (fitz) | PDF 渲染为图片 | `python -c "import fitz; print(fitz.__doc__[:50])"` |

如果 PyMuPDF 没装：

```powershell
pip install pymupdf
```

skill 内部已经写了 fallback：如果 PyMuPDF 不可用，会跳过图片、用 Mermaid 重画流程图（少几张图但不会失败）。

---

## 五、常见问题排查

### Q1. Skill 没触发怎么办？
- 检查 `~/.claude/skills/pdf-lecture-to-obsidian/SKILL.md` 是否存在
- 在对话里**直接说**："请用 pdf-lecture-to-obsidian skill 处理 …"
- 或在新会话开始时直接点 `/skills` 看 skill 是否在列表里

### Q2. 中文路径报错？
SKILL.md 里已经强调过：路径包含非 ASCII 字符时优先用 Read/Write/Glob 工具，不用 shell 命令。如果还是遇到，可以临时把中文路径软链接到 ASCII 路径。

### Q3. PDF 太大，提取慢？
- 在 prompt 里限制范围："只看前 30 页"
- 或在 `extract_pdf_pages.py` 里手动指定 `--zoom 1.0`（降画质换速度）

### Q4. Obsidian 显示图片是 broken link？
- 检查图片路径是否相对 vault root（不是相对 .md 文件）
- 例如 vault = `F:\我的笔记\`，图片在 `F:\我的笔记\附件\图片\xxx.png`，正确写法：`![[附件/图片/xxx.png]]`
- 反斜杠改正斜杠

### Q5. 生成的笔记不够"我的风格"？
看下面"如何持续迭代"。

---

## 六、如何持续迭代 skill

第一次跑不会完美。你用过几次后会发现想改的地方。

### 反馈循环
1. 用过一次 → 记下不满意的地方（比如"例题太少"、"公式没加引用"）
2. 在新会话里说："改一下 pdf-lecture-to-obsidian skill — XXX 不好"
3. Claude 会用 skill-creator 调用它来改 SKILL.md / 模板

### 如果想正式迭代（带量化评估）
```
跑一下 pdf-lecture-to-obsidian skill 的评估，
之前的测试我看后留 feedback 在 feedback.json 里
```

Claude 会用 `skill-creator` 工作流跑下一轮 with-skill vs without-skill 对比、生成 eval viewer 给你看。

---

## 七、如何分享给别人

Skill 是单文件夹结构，可以直接复制。

### 方法 A — 打包为 `.skill` 文件
```
python C:\Users\lenovo\.claude\plugins\cache\claude-plugins-official\skill-creator\unknown\skills\skill-creator\scripts\package_skill.py C:\Users\lenovo\.claude\skills\pdf-lecture-to-obsidian
```
得到 `pdf-lecture-to-obsidian.skill` 文件，发给同学。对方安装即可。

### 方法 B — 直接拷贝整个文件夹
对方把整个 `pdf-lecture-to-obsidian/` 复制到自己的 `~/.claude/skills/` 下即可。

### 方法 C — 推到 git
```
cd C:\Users\lenovo\.claude\skills\pdf-lecture-to-obsidian
git init
git add .
git commit -m "Initial skill"
git remote add origin <your-repo>
git push
```
别人 `git clone` 到 `~/.claude/skills/` 下即可。

---

## 八、Skill 文件清单（供你心里有数）

```
pdf-lecture-to-obsidian/
├── SKILL.md                              ← 主文件（800 行，描述工作流）
├── USAGE.md                              ← 本文件
├── scripts/
│   └── extract_pdf_pages.py              ← PDF 转 PNG 通用工具
├── references/
│   ├── main_note_template.md             ← 主笔记模板
│   ├── example_template.md               ← 例题文件模板
│   ├── overview_template.md              ← 总览文件模板
│   ├── mock_exam_template.md             ← 模拟卷模板
│   └── workflow_checklist.md             ← 工作流速查
└── evals/
    ├── evals.json                        ← 行为测试用例
    └── trigger_eval.json                 ← 描述/触发测试用例
```

`evals/` 在日常使用时用不到，只在迭代评估时启用。

---

## 九、未来扩展的想法（仅作记录，不必现在做）

| 想法 | 难度 |
|------|------|
| 加 PPT 输入支持（.pptx → 笔记）| 中 |
| 加 OCR 支持（扫描版 PDF）| 高 |
| 加多语言翻译开关（中→英、英→中）| 中 |
| 加"按章节切分笔记"模式（一份 PDF 切成多份笔记）| 中 |
| 加自动 Anki 卡片导出 | 低 |
| 加自动 push 到 git 仓库 | 低 |

---

## 十、给我自己的「下一步」备忘

- [ ] 跑 1 次后看看输出质量是否符合期望
- [ ] 如果发现"例题太敷衍"等具体问题，让 Claude 改 `references/example_template.md`
- [ ] 整个学期把所有课都用这个 skill 处理一遍
- [ ] 学期结束做一次大复盘，把累积的改进沉淀回 SKILL.md

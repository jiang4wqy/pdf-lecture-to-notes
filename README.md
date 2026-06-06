# pdf-lecture-to-notes

> 把一整门课的 PDF 课件，一键变成结构清晰、考点齐全的复习笔记 —— **Obsidian 双向链接版**或 **Word(.docx) 版**，运行时任选。
>
> A [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) skill that turns a folder of lecture PDFs into an exam-ready study notebook, in your choice of format: an Obsidian-style linked vault, or a Word document (rendered via pandoc).

> 📦 本仓库原名 `pdf-lecture-to-obsidian`，因新增 Word 输出已更名为 `pdf-lecture-to-notes`。旧链接由 GitHub 自动重定向。

---

## ✨ 这个 skill 能做什么

给它一个**装满课件 PDF 的文件夹**（lecture slides、复习提纲、模拟题都行），它会自动产出一整套互相链接的 Markdown 笔记：

```
你的笔记库/<课程>/
├── 00_总览.md                ← 索引页：所有笔记 + 考试地位映射 + 推荐学习顺序
├── 01_xxx.md                 ← 主笔记（每节课一份）
├── 02_xxx.md                       含定义、公式、例题、对比表、易错点、速记卡
├── 03_xxx.md
├── ...
├── 99_综合模拟卷.md          ← 可选：基于练习题 PDF 整合的模拟卷
└── 例题与考点/
    ├── 01_xxx_例题与考点.md  ← 与主笔记双向 [[wiki-link]]
    ├── 02_xxx_例题与考点.md
    └── ...

你的笔记库/附件/图片/<课程>/
├── 关键公式_p7.png           ← 自动从 PDF 提取的关键页（公式/流程图/对比表）
├── 流程图_p12.png
└── ...
```

每份主笔记自带：
- `> [!info] 考试地位` 标注 ⭐⭐⭐ 级别
- 关键公式以 `$$...$$` 渲染，并截图嵌入到 Obsidian
- "易错点" 区块、"必背速记卡" 区块
- 与例题文件、其他主笔记的双向 `[[]]` 链接

### 📄 也能导出 Word

同一套内容可以渲染成 **Word(.docx)**（用 pandoc，公式转 Word 原生公式、图片内嵌、自动目录）：

- **整门课一份** `.docx`：封面 + 目录 + 所有讲次 + 例题附录，适合打印 / 发给同学 / 当作业交。
- **一课一份** `.docx`：每讲单独一个文件，配套例题作附录。

Markdown 始终是唯一内容源，Word 由它转换而来——**笔记只生成一次**。

---

## 🚀 安装（30 秒）

### 前置依赖：
- 已安装 [Claude Code](https://claude.com/claude-code)
- Python ≥ 3.8（图片提取）
- **pandoc**（仅 Word 输出需要，不是 pip 包）：
  - Windows: `winget install --id JohnMacFarlane.Pandoc`
  - macOS: `brew install pandoc`
  - Linux: `sudo apt install pandoc`
  - 只用 Obsidian 输出可以不装 pandoc。

### 步骤：

**Windows (PowerShell)**
```powershell
cd $env:USERPROFILE\.claude\skills
git clone https://github.com/jiang4wqy/pdf-lecture-to-notes.git
pip install -r pdf-lecture-to-notes\requirements.txt
```

**macOS / Linux**
```bash
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/jiang4wqy/pdf-lecture-to-notes.git
pip install -r pdf-lecture-to-notes/requirements.txt
```

重启 Claude Code。skill 会自动被发现，不需要任何额外注册。

> 用 `/skills` 命令可以确认 `pdf-lecture-to-notes` 在列表里。

---

## 🎯 使用：直接对 Claude 说话

skill 会根据你说的话自动触发。例如：

```
把 C:\Users\me\Desktop\金融概论\ 里的 PDF 做成 Obsidian 笔记，
放到 F:\我的笔记\corporate-finance\，图片放 F:\我的笔记\附件\图片\。
```

或者要 Word 版：

```
把「机器学习」这门课的 PDF 做成一份 Word 复习册（整门课一份 .docx）
```

Claude 会先：
1. 列出输入文件夹下的所有 PDF，识别复习提纲 / 练习题 / 正课课件
2. 给你一个**计划**（建议的文件结构、是否要例题文件夹、是否要模拟卷）
3. **问你要哪种输出**：Obsidian（默认）/ Word 整门课一份 / Word 一课一份
4. **等你确认**后才动手

确认后它会跑完整工作流（提取图片 → 写主笔记 → 写例题 → 写总览 → 加交叉链接 → 选 Word 则再转 docx），最后给你一份汇总：文件数、行数、图片数、建议从哪份打开。

> 📖 详细使用场景（新课程 / 单 PDF / 补充已有课程）见 [USAGE.md](USAGE.md)。

---

## ⚙️ 工作原理（两段式）

**Part A — 格式无关核心**（无论出哪种格式都跑）：

| Step | 它在干什么 |
|------|-----------|
| 1. Discover | 扫描输入文件夹，按文件名关键词（`review` / `复习` / `practice` / `模拟`）分类 PDF |
| 2. Plan | 读复习提纲 → 整理出官方模块结构 → 提议笔记列表 → **等用户确认** |
| 2.5 选格式 | 问用户要 Obsidian（默认）/ Word 整门课一份 / Word 一课一份 |
| 3. Extract images | 用 `scripts/extract_pdf_pages.py`（PyMuPDF）智能挑出含公式/流程图/对比表的页，渲染为 PNG |
| 4. Write notes | 按 `references/` 下的模板生成主笔记、例题、总览、模拟卷（Obsidian 风格 markdown，唯一内容源） |

**Part B — 按格式分支**：

| 分支 | 它在干什么 |
|------|-----------|
| B-Obsidian | 全局扫描插入 `[[]]` 交叉链接 → 校验文件/链接/图片 → 报告 |
| B-Word | 交叉链接后，用 `scripts/build_docx.py`（pandoc）把 markdown 转 .docx，校验后报告 |

完整工作流和"为什么这么设计"详见 [SKILL.md](SKILL.md)；Word 细节见 [references/word_output_guide.md](references/word_output_guide.md)。

---

## 📂 仓库结构

```
pdf-lecture-to-notes/
├── SKILL.md                          ← skill 的核心（描述 + 工作流），Claude 自动读取
├── USAGE.md                          ← 给最终用户看的使用指南（场景、FAQ、迭代方法）
├── README.md                         ← 本文件
├── LICENSE                           ← MIT
├── requirements.txt                  ← Python 依赖（PyMuPDF）；Word 另需 pandoc
├── .gitignore
├── scripts/
│   ├── extract_pdf_pages.py          ← 批量 PDF→PNG 工具，由 SKILL 工作流调用
│   └── build_docx.py                 ← markdown→Word(.docx) 转换器（pandoc 包装）
├── references/                       ← 笔记模板 + 工作流速查 + Word 指南
│   ├── main_note_template.md
│   ├── example_template.md
│   ├── overview_template.md
│   ├── mock_exam_template.md
│   ├── workflow_checklist.md
│   └── word_output_guide.md          ← Word 分支细节（pandoc 用法、语法转换、样式）
└── evals/                            ← skill 行为评估用例（日常使用无需关心）
    ├── evals.json
    └── trigger_eval.json
```

---

## 🔧 自定义

所有可改项都在 [SKILL.md](SKILL.md) 的 **"Default decisions baked into this skill"** 表里。常见改动：

| 想改什么 | 改哪里 |
|---------|-------|
| 默认输出 Obsidian / Word | "Output target" 行 |
| 不要 Obsidian wiki-link，改用标准 Markdown | "Output format" 行 |
| 总是生成例题文件夹，不再每次问 | "例题与考点 sub-folder" 行 |
| 每份笔记更短/更长 | "Note size" 行 |
| 图片提取的画质（默认 144 DPI） | `scripts/extract_pdf_pages.py` 的 `--zoom` 参数 |
| Word 的字体/标题样式 | 生成 `reference.docx` 并传 `--reference`（见 word_output_guide.md） |
| Word callout 标签文字 | `scripts/build_docx.py` 的 `CALLOUT_LABELS` 字典 |

也可以直接在调用时通过 prompt 临时覆盖，例如："要求每份笔记至少有 10 张配图"。

---

## 🩺 常见问题

**Q: skill 没自动触发？**
在对话里直接说："请用 `pdf-lecture-to-notes` skill 处理 ..."。或先 `/skills` 确认它在列表中。

**Q: 提示 `ModuleNotFoundError: No module named 'fitz'`**
运行 `pip install pymupdf`。如果不想装也行——skill 内置了 fallback：跳过图片，改用 Mermaid 重画流程图。

**Q: 导出 Word 时提示 `pandoc not found`？**
Word 输出需要 pandoc（不是 pip 包）：`winget install --id JohnMacFarlane.Pandoc`（Win）/ `brew install pandoc`（mac）/ `sudo apt install pandoc`（Linux）。装完重开终端。只用 Obsidian 输出则无需 pandoc。

**Q: Word 里公式变成乱码 / 没渲染？**
确认源 markdown 用的是 `$...$` / `$$...$$`（pandoc 才能转 Word 原生公式）。普通文本里的 `$`（如 `$5000`）不受影响。

**Q: Obsidian 里图片显示 broken link？**
检查图片路径是否相对于 vault 根目录。例如 vault = `F:\我的笔记\`，图片在 `F:\我的笔记\附件\图片\xxx.png`，正确写法是 `![[附件/图片/xxx.png]]`（用正斜杠）。

**Q: 中文路径报错？**
让 Claude 优先用 Read/Write/Glob 工具而不是 shell 命令处理路径——SKILL.md 里已有这条指导。

更多 FAQ 见 [USAGE.md 第五节](USAGE.md)。

---

## 🤝 贡献 / 反馈

发现 skill 输出有问题，或想加新功能：
- 直接开 [Issue](https://github.com/jiang4wqy/pdf-lecture-to-notes/issues)
- 或 Fork 改完发 PR

也欢迎分享你用这个 skill 整理出来的笔记结构截图——可以帮我们持续优化模板。

---

## 📜 License

[MIT](LICENSE) — 随意用、改、分发，标个原作者就行。

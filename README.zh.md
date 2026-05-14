# handwritten-math-notes-skill

将**手写版或扫描版数理课程笔记**（PDF）转录为结构清晰的 Markdown，公式使用标准 LaTeX。

与通用 PDF 转 Markdown 工具不同，本工具专为课堂场景设计：教授手写的大量数学符号——矩阵、范数、希腊字母、上下标、证明结构——都能被准确识别。它跳过了脆弱的传统 OCR 流程，直接通过多模态大模型以视觉方式读取 PDF 页面。

## 核心差异

- **手写体优先** — 针对中英文混排、手写数学公式密集的课堂笔记 PDF 优化
- **视觉直读** — 将 PDF 页面作为图像直接输入底层多模态大模型，避免 OCR 误识别
- **LaTeX 原生输出** — 所有公式使用标准 LaTeX：`$...$` 行内、`$$...$$` 独立公式
- **结构保真** — 完整保留章节、定理、引理、证明（含 `\square`）、定义、注记、算法块
- **智能分页** — 一次读取 ≤15 页；对大 PDF 自动切分图片分批处理

## 已验证模型

转录质量完全取决于底层多模态视觉能力。本 Skill 已在 **kimi 2.6** 上完整测试并通过。任何具备同等视觉推理能力的大模型也应可用。

> **注意：** 本仓库包含的是 *Claude Code Skill 定义文件*（编排逻辑）。实际的页面阅读与转录智能来自你运行时所使用的多模态大模型。

## 前置依赖

- [Claude Code](https://claude.ai/code) CLI（用于托管 Skill）
- 具备多模态能力的大模型后端（已在 **kimi 2.6** 上验证）
- Python 3 + `pymupdf`（仅用于页数统计与大 PDF fallback）

```bash
pip install pymupdf
```

## 安装

1. 克隆本仓库：

```bash
git clone https://github.com/yourusername/handwritten-math-notes.git
```

2. 将 Skill 文件复制到 Claude Code 命令目录：

```bash
cp handwritten-math-notes/pdf-to-md.md ~/.claude/commands/
```

3. 复制大 PDF 处理脚本（可选，>30 页时需要）：

```bash
mkdir -p ~/.claude/scripts
cp handwritten-math-notes/pdf-to-images.py ~/.claude/scripts/
```

4. 重启 Claude Code 或开启新会话，即可使用 `/pdf-to-md` 命令。

## 使用

在 Claude Code 会话中输入：

```
/pdf-to-md <pdf路径> [输出md路径]
```

若省略输出路径，默认在 PDF 同级目录生成同名 `.md` 文件。

### 示例

```
/pdf-to-md ~/Course/数值代数/lecture7.pdf
/pdf-to-md ~/notes/期中复习.pdf ~/notes/期中复习_clean.md
```

## 工作流程

1. **页数检查**：使用 `pymupdf` 获取 PDF 总页数
2. **视觉读取**：将 PDF 页面渲染为图像，输入多模态大模型
3. **上下文转录**：模型结合数学上下文理解手写内容，自动校正歧义（如区分 `ρ` 与 `p`，识别迭代下标）
4. **结构化输出**：生成含标题层级、定理/证明块、算法伪代码、LaTeX 公式的 Markdown
5. **文件写入**：保存到指定路径

## 传统 OCR vs. 视觉直读

| 场景 | 传统 OCR | 视觉直读（本 Skill） |
|:---|:---|:---|
| 希腊字母 | `ρ` 误识为 `p`，`σ` 误识为 `o` | 结合上下文正确识别 |
| 上下标 | `x_i^{(k)}` 误为 `x_n^{(k)}` | 精确还原索引关系 |
| 中英文混排 | “送代”等形近错字 | 原生多语言推理 |
| 矩阵结构 | 对齐错乱、缺失定界符 | 标准 `pmatrix` / `bmatrix` |
| 证明结构 | 扁平文本，丢失 Q.E.D. | 保留层次，使用 `\square` 结尾 |
| 行列式与范数 | `\|` 与 `\|` 混用 | 根据语义正确使用 `\det`、`|·|` |

## 项目结构

```
handwritten-math-notes/
├── pdf-to-md.md          # Claude Code Skill 定义文件
├── pdf-to-images.py      # 大 PDF 转图片 fallback 脚本
├── README.md             # English readme
└── README.zh.md          # 中文 readme
```

## 输出规范

- `#` 标题（课程/讲座主题 + 日期）
- `##` / `###` 章节层次与原始大纲一致
- `**定理**`、`**引理**`、`**证明**：` … `\square` 标记数学区块
- `**定义**`、`**注**` 标记关键概念
- `---` 分隔主要章节
- 算法伪代码使用 ``` 代码块

## 许可

MIT

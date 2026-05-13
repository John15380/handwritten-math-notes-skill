---
argument-hint: <pdf-path> [output-md-path]
description: Convert handwritten/printed math lecture notes (PDF) to well-formatted Markdown with LaTeX
---

# /pdf-to-md — 数理手稿/课件 PDF → Markdown

将扫描版或手写版数理课程 PDF（尤其是含大量数学公式的课堂笔记/课件）转换为结构清晰的 Markdown，公式使用 LaTeX。

## 触发条件

用户提到：
- "convert PDF to markdown"
- "把课件转成笔记"
- "整理这份手稿"
- 或提供 `.pdf` 路径并要求转录/整理

## 前置检查

```bash
python3 -c "import fitz" 2>/dev/null || pip3 install --break-system-packages pymupdf 2>/dev/null || pip3 install pymupdf
```

## 处理流程

### Step 1: 获取页数

```bash
python3 -c "import fitz, sys; print(fitz.open(sys.argv[1]).page_count)" "<pdf-path>"
```

### Step 2: 读取 PDF

**直接视觉读取（推荐）**：使用 Read 工具读取 PDF。根据页数选择策略：

- **≤ 15 页**：一次性读取全部页
  ```tools
  Read: file_path="<pdf-path>", pages="1-<N>"
  ```

- **16–30 页**：分两批读取
  - 第一批：`pages="1-15"`
  - 第二批：`pages="16-<N>"`

- **> 30 页**：先转图片再读取（避免上下文过长）
  ```bash
  python3 ~/.claude/scripts/pdf-to-images.py "<pdf-path>" /tmp/pdf_pages 300
  ```
  然后用 Read 工具读取 `/tmp/pdf_pages/page_*.png`，每批不超过 15 张。

**读取策略**：尽量按页码顺序处理，保持笔记的连续性。

### Step 3: 转录整理

读取完所有页面后，整理为 Markdown。要求：

**数学公式**
- 所有数学表达式用 LaTeX：`$...$` 行内，`$$...$$` 独立公式
- 矩阵用 `\begin{pmatrix}...\end{pmatrix}` 或 `\begin{bmatrix}...\end{bmatrix}`
- 范数 `\|x\|`，谱半径 `\rho(M)`，极限 `\lim\limits_{k \to \infty}`
- 下标 `a_{ij}`，上标 `x^{(k)}`，求和 `\sum_{i=1}^n`
- 增广矩阵可用 `\left(\begin{array}{ccc|c}...\end{array}\right)`

**结构层次**
- `#` 标题（课程/讲座主题）
- `##` 大节（如 "第一章 xxx"）
- `###` 小节（如 "§1.1 xxx"）
- `**定义**` / `**定理**` / `**命题**` / `**引理**` / `**推论**` 标记重要区块
- `**证明**：` ... `\square` 结尾
- `**注**：` 或 `**Remark**：` 标记备注
- `---` 分隔主要章节

**内容校对**
- 忠实于原文，不遗漏定理、公式、例子
- 手写体识别后结合数学上下文校正（如确认是 "迭代" 而非 "送代"）
- 保留例题编号和算法步骤
- 算法伪代码用 ``` 代码块

### Step 4: 写入文件

将整理好的 Markdown 写入 `[output-md-path]`。若未指定，默认在 PDF 同级目录生成同名 `.md` 文件。

写入后验证文件存在，并告知用户输出路径和总页数。

## 示例

```
/pdf-to-md "~/Course/5数值代数/3正定矩阵的平方根法及推广.pdf"
/pdf-to-md "~/notes/lecture5.pdf" "~/notes/lecture5_clean.md"
```

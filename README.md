# handwritten-math-notes-skill

A Claude Code custom skill that transcribes **handwritten or scanned math lecture notes** (PDF) into well-structured Markdown with LaTeX math.

Unlike generic PDF-to-Markdown converters, this tool is purpose-built for academic settings where professors write dense mathematical notation—matrices, norms, Greek letters, subscripts, and proof structures—by hand. It skips brittle OCR pipelines and reads PDF pages visually through a large multimodal model.

## What makes it different

- **Handwriting-first** — Optimized for lecture PDFs with mixed Chinese text and handwritten math
- **Visual ingestion** — Feeds PDF pages as images directly to the underlying multimodal LLM, avoiding OCR misreads
- **LaTeX-native output** — All formulas in standard LaTeX: `$...$` inline and `$$...$$` display
- **Structure preserved** — Sections, theorems, lemmas, proofs (with `\square`), definitions, remarks, and algorithm blocks are all kept intact
- **Smart paging** — Reads ≤15 pages at once; falls back to image slicing for larger PDFs

## Verified model

The transcription quality depends entirely on the underlying multimodal vision capability. This skill has been **fully tested and validated on kimi 2.6**. It should also work with any other large model that offers comparable visual reasoning.

> **Note:** This repository contains the *Claude Code skill definition* (the orchestration logic). The actual page-reading intelligence comes from the multimodal model you run it with.

## Prerequisites

- [Claude Code](https://claude.ai/code) CLI (to host the skill)
- A multimodal-capable backend model (tested on **kimi 2.6**)
- Python 3 with `pymupdf` (page counting and large-PDF fallback only)

```bash
pip install pymupdf
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/handwritten-math-notes.git
```

2. Copy the skill file into your Claude Code commands directory:

```bash
cp handwritten-math-notes/pdf-to-md.md ~/.claude/commands/
```

3. Copy the fallback script (optional, for PDFs > 30 pages):

```bash
mkdir -p ~/.claude/scripts
cp handwritten-math-notes/pdf-to-images.py ~/.claude/scripts/
```

4. Restart Claude Code or start a new session.

## Usage

Inside a Claude Code session:

```
/pdf-to-md <pdf-path> [output-md-path]
```

If `output-md-path` is omitted, a `.md` file is created next to the PDF.

### Examples

```
/pdf-to-md ~/Course/NumericalAlgebra/lecture7.pdf
/pdf-to-md ~/notes/midterm_review.pdf ~/notes/midterm_review_clean.md
```

## How it works

1. **Page inspection** — `pymupdf` counts pages
2. **Visual reading** — PDF pages are rendered and fed to the multimodal model as images
3. **Contextual transcription** — The model interprets handwritten math in context, resolving ambiguities (e.g., `ρ` vs `p`, iteration indices vs variable names)
4. **Structured Markdown** — Headings, theorem/proof blocks, algorithms, and LaTeX equations are emitted
5. **File write** — Saved to the specified path

## Traditional OCR vs. visual transcription

| Scenario | Traditional OCR | Visual transcription (this skill) |
|:---|:---|:---|
| Greek letters | `ρ` → `p`, `σ` → `o` | Correct via visual context |
| Sub/superscripts | `x_i^{(k)}` → `x_n^{(k)}` | Precise index recognition |
| Mixed CJK + math | “送代” instead of “迭代” | Native multilingual reasoning |
| Matrix layout | Broken alignment, missing delimiters | Proper `pmatrix` / `bmatrix` |
| Proof structure | Flat text, missing Q.E.D. | Preserved hierarchy with `\square` |
| Determinants vs. norms | `||` misread as brackets | Semantically correct `\det`, `\|\cdot\|` |

## Project structure

```
handwritten-math-notes/
├── pdf-to-md.md          # Claude Code skill definition
├── pdf-to-images.py      # Large-PDF image fallback script
├── README.md             # English readme
└── README.zh.md          # 中文 readme
```

## Output conventions

- `#` Title (lecture topic + date)
- `##` / `###` Section hierarchy matching the original outline
- `**Theorem**`, `**Lemma**`, `**Proof**:` … `\square` for math blocks
- `**Definition**`, `**Remark**` for key concepts
- `---` between major sections
- Algorithms in fenced code blocks

## License

MIT

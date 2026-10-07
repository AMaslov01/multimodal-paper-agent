# Multimodal Scientific Paper Agent

A retrieval-augmented agent that answers questions about scientific papers from
LaTeX source, equations, tables, and figures. It was built for a hackathon with
GigaChat-2-Max, a fixed answer format, and a 15-minute runtime limit.

## How it works

1. Discovers the LaTeX entry point and expands nested `\input`/`\include` files.
2. Extracts sections, equations, captions, labels, and cross-references.
3. Converts paper figures to images and produces searchable visual descriptions.
4. Builds section-aware chunks and indexes them with GigaChat embeddings in ChromaDB.
5. Uses a LangGraph workflow to plan retrieval, search likely sections, inspect a
   figure when needed, and compose an evidence-grounded answer.
6. Falls back to a global search when scoped evidence is weak and writes a valid
   placeholder when the available paper context does not support an answer.

Intermediate artifacts, embeddings, and prior answers are cached per paper. The
repository also includes an evaluation harness for retrieval coverage, synthetic
recall@5, figure hit rate, latency, and answer self-checks.

## Repository layout

```text
run.py                 Entry point and output guarantees
src/ingest/            LaTeX discovery, parsing, figures, and chunking
src/index/             Embeddings, ChromaDB storage, and retrieval
src/agent/             LangGraph workflow and prompts
src/cache/             Paper and question-answer caches
src/io/                Question parsing and answer formatting
src/utils/eval.py      Local evaluation harness
```

## Setup

Python 3.10-3.13 and [`uv`](https://docs.astral.sh/uv/) are recommended.

```bash
uv sync --frozen
cp .env.example .env
```

Add your own GigaChat credentials to `.env`:

```bash
GIGACHAT_CREDENTIALS='...'
GIGACHAT_SCOPE='GIGACHAT_API_CORP'
```

Never commit `.env` or a real credential.

## Run

Place the paper materials and `questions.txt` in `data/`, then execute:

```bash
uv run python run.py
uv run python -m src.utils.check_submission
```

Answers are written to `output/answers.txt`. Both numbered questions and
`## Question N` Markdown blocks are supported; output preserves the matching
format and contains one answer block per question.

## Evaluation and tests

The evaluation harness requires configured GigaChat credentials:

```bash
uv run python -m src.utils.eval --article-dir data --mode all
```

The unit suite is offline and does not access model endpoints:

```bash
python -m unittest discover -s tests -v
```

## Limitations

- LaTeX parsing is heuristic rather than a full TeX interpreter.
- Figure understanding depends on successful rendering and the vision model.
- Retrieval thresholds were tuned for the original challenge data and may need
  recalibration for other corpora.
- A broad-context fallback uses only material already loaded from the paper;
  unsupported questions return `no answer`.

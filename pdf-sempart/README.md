
# pdf-sempart

**pdf-sempart** is a modular Python package for layout-aware semantic chunking of PDFs, using true hierarchical topic modeling (tomotopy hLDA) and dual embeddings (E5, GTE) with a strict 3-way voting boundary rule. It is designed for robust, multi-column document segmentation and sectionization, and outputs a DocMap-style JSON for downstream use.

---

## Features

- **Input:** Dicts from [dots.ocr](https://github.com/rednote-hilab/dots.ocr): `{text|table|image}` lists with `page`, `bbox`, `content`, `font_size`, `is_bold`.
- **Pipeline:**
  - Multi-column reading order (KMeans)
  - Paragraph merging (layout + semantic continuity)
  - hLDA topic tree per document
  - Dual embeddings (E5, GTE)
  - 3-way voting for chunk boundaries
  - Section tree from headings + boundaries
  - DocMap JSON output
- **Configurable:** All thresholds, model IDs, and hLDA parameters are in `config/defaults.yaml`.
- **CLI:** Run the full pipeline from the command line.
- **Tested:** Unit tests for all major modules.

---

## Installation

Clone the repo and install dependencies:

```bash
git clone <repo-url>
cd pdf-sempart
make setup
```

---

## Usage

Run the demo pipeline on example input:

```bash
make run-demo
# or manually:
python -m pdf_sempart.cli.sempart \
  --in examples/demo_input.json \
  --out examples/demo_docmap.json \
  --config config/defaults.yaml
```

**Input:** JSON dict with `text`, `table`, `image` lists (see `examples/demo_input.json`).

**Output:** DocMap-style JSON with `sections` and `chunks` (see `examples/demo_docmap.json`).

---

## Configuration

All pipeline parameters (model IDs, thresholds, hLDA settings) are in `config/defaults.yaml`. You can override this with `--config`.

---

## Module Overview

**src/pdf_sempart/**

- `cli/sempart.py` — CLI entrypoint. Loads config, input, runs pipeline, writes output.
- `io/schema.py` — DocMap dataclasses, validation, and serialization.
- `io/loaders.py` — Input validation and conversion to Block objects.
- `io/writer.py` — Save DocMap as JSON.
- `layout/blocks.py` — Block dataclass (text/table/image, page, bbox, etc).
- `layout/order.py` — Multi-column detection (KMeans) and reading order logic.
- `layout/merge.py` — Merge blocks into paragraphs using layout and semantic continuity.
- `nlp/preprocess.py` — Text normalization and tokenization.
- `nlp/headings.py` — Heading detection and level scoring (font z-score, numbering, ALL-CAPS).
- `topics/hlda.py` — tomotopy.HLDAModel adapter for hierarchical topic modeling.
- `embed/encoder_a.py` — Embedding model A (default: E5-small).
- `embed/encoder_b.py` — Embedding model B (default: GTE-small).
- `boundaries/voter.py` — 3-way voting for chunk boundaries (topic + 2 embeddings).
- `sectionize/build.py` — Build section tree (H1/H2/H3) from headings and boundaries.
- `pipeline/run.py` — Orchestrates the full pipeline: loading, merging, embedding, topic modeling, boundary detection, sectionization, and output.

---

## Test Suite

All major modules have unit tests in `tests/`:

- `test_order.py` — Ensures multi-column reading order is left→right, top→bottom.
- `test_merge.py` — Checks that sentence-ending + low cosine triggers paragraph split.
- `test_hlda.py` — Verifies hLDA trains and outputs non-empty topic paths for toy data.
- `test_boundaries.py` — Synthetic topic/embedding sequences trigger 3-way boundary at expected indices.
- `test_sectionize.py` — Numbered/bold/large fonts become H1/H2/H3 and nesting is correct.

Run all tests:

```bash
make test
# or
pytest -q
```

---

## Example Input

```json
{
  "text": [
    {"page": 1, "bbox": [50, 100, 550, 120], "content": "Introduction", "font_size": 16, "is_bold": true},
    {"page": 1, "bbox": [50, 130, 550, 150], "content": "This is a demo paragraph about PDF chunking.", "font_size": 12, "is_bold": false}
  ],
  "table": [],
  "image": []
}
```

---

## Output DocMap

The output is a JSON with `meta`, `sections`, and `chunks`. Each chunk contains its section path, topic node IDs, topic weight, and paragraph metadata.

---

## License

MIT License

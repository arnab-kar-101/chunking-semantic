# chunking-semantic

**Project Overview**
- `pdf-sempart/` contains a modular pipeline for layout-aware semantic chunking of PDFs.
- Goal: convert OCR-style inputs into DocMap JSON with sections, hierarchical topics, and chunk metadata.
- Architecture favors swappable components (layout, embeddings, topics) and tight unit/integration coverage.

**Repo Layout**
- `pdf-sempart/README.md` — package-specific guide; mirrors CLI usage and module descriptions.
- `pdf-sempart/src/pdf_sempart/` — production code organised by concern:
  - `cli/sempart.py` CLI entrypoint.
  - `io/` loaders + schema + writer utilities.
  - `layout/` column ordering + paragraph merging.
  - `embed/` dual encoder adapters (lazy SentenceTransformer loading).
  - `nlp/` preprocessing + heading detection.
  - `topics/` pluggable hLDA wrapper (stub by default, optional tomotopy backend).
  - `boundaries/` 3-way voter combining topics + embeddings.
  - `sectionize/` heading tree assembler + section path resolution.
  - `pipeline/run.py` orchestrates the full document flow end-to-end.
- `pdf-sempart/tests/` — focused unit tests plus integration suites exercising sample data.
- `presentations/` — Graphviz `.dot` diagrams capturing module dependencies (`pdf_sempart_module_structure.dot`) and pipeline flow (`pdf_sempart_pipeline_flow.dot`).

**Pipeline Flow**
- Load OCR-style JSON → normalize into Block objects (`io.loaders`).
- Order blocks by page/column using heuristic column-gap detection (`layout.order`).
- Merge blocks into paragraphs with layout + semantic continuity checks (`layout.merge`).
- Encode paragraphs with two SentenceTransformers (`embed.encoder_a/b`).
- Tokenise text and infer hierarchical topics via the hLDA wrapper (`nlp.preprocess`, `topics.hlda`).
- Vote chunk boundaries using topic drift + embedding similarity (`boundaries.voter`).
- Score headings and assemble section tree (`nlp.headings`, `sectionize.build`).
- Build DocMap chunks, attach metadata, optionally persist JSON (`pipeline.run`, `io.writer`).
- DOT diagrams in `presentations/` can be rendered via `dot -Tsvg presentations/pdf_sempart_pipeline_flow.dot -o flow.svg`.

**Setup & Installation**
- Requires Python 3.9+.
- Recommended workflow:
  - `cd pdf-sempart`
  - `python3 -m venv .venv && source .venv/bin/activate`
  - `pip install -e .` (installs core deps: `sentence-transformers`, `PyYAML`).
- Optional extras:
  - `pip install .[dev]` for linting/type-check/test tooling.
  - `pip install .[topics]` and set `PDF_SEMPART_TOPIC_BACKEND=tomotopy` to enable the native tomotopy HLDA backend (otherwise stubbed logic is used).

**Running the Pipeline**
- Demo: `make run-demo` (loads `examples/demo_input.json`, writes `examples/demo_docmap.json`).
- Manual CLI invocation:
  ```bash
  python -m pdf_sempart.cli.sempart \
    --in path/to/input.json \
    --out path/to/output.json \
    --config config/defaults.yaml
  ```
- Configuration toggle points sit in `config/defaults.yaml` (model IDs, thresholds, hLDA params).

**Testing**
- Quick run: `python3 -m pytest` from within `pdf-sempart/` (11 tests covering layout, merging, topics stub, IO, section building, and both demo + sample end-to-end flows).
- New integration tests target:
  - `tests/test_pipeline_integration.py` (stubbed embeddings over `tests/data/sample_report.json`).
  - `tests/test_pipeline_sample.py` (drives `examples/sample.json`).
- Unit tests validate individual modules (`test_boundaries.py`, `test_order.py`, `test_merge.py`, `test_headings.py`, etc.).

**Development Notes**
- Encoders lazy-load models, enabling fast tests with mocks.
- Layout/statistical utilities avoid heavy numeric dependencies, easing deployment to constrained envs.
- Graphviz diagrams kept in version control; regenerate exported images from `.dot` when sharing documentation.

# chunking-semantic

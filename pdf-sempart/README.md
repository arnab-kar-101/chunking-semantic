# pdf-sempart

Layout-aware semantic chunking for PDFs using true hierarchical topics (tomotopy hLDA) and dual embeddings (E5, GTE) with a strict 3-way voting boundary rule.

- **Input:** Dicts from dots.ocr: `{text|table|image}` lists with `page`, `bbox`, `content`, `font_size`, `is_bold`.
- **Pipeline:**
  - Multi-column reading order (KMeans)
  - Paragraph merging (layout + semantic)
  - hLDA topic tree per document
  - Dual embeddings (E5, GTE)
  - 3-way voting for chunk boundaries
  - Section tree from headings + boundaries
  - DocMap JSON output

See `examples/run.sh` for usage. All config is in `config/defaults.yaml`.

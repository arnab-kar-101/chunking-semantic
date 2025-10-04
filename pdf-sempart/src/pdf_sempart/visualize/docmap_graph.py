"""Utilities for visualising DocMap sections around specific page ranges.

The main entrypoint, :func:`generate_section_tree_dot`, accepts a DocMap-like
structure (as produced by ``pdf_sempart.pipeline.run.process_document``), a
target page range, and emits Graphviz DOT text capturing the relevant section
hierarchy and paragraphs. Pages immediately before/after the requested window
can be included via ``context_pages`` to provide surrounding structure.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple


@dataclass
class ParagraphView:
    idx: int
    page: int
    section_path: Tuple[str, ...]
    text: str


def _normalise_section_path(raw_path: Sequence[str]) -> Tuple[str, ...]:
    cleaned = tuple(part for part in raw_path if part)
    if cleaned:
        return cleaned
    return ("(No Section)",)


def _collect_paragraphs(docmap: Dict) -> List[ParagraphView]:
    paragraphs: List[ParagraphView] = []
    idx = 0
    for chunk in docmap.get("chunks", []):
        section_path = _normalise_section_path(chunk.get("section_path", []))
        for para in chunk.get("paras", []):
            paragraphs.append(
                ParagraphView(
                    idx=idx,
                    page=int(para.get("page", 0) or 0),
                    section_path=section_path,
                    text=str(para.get("text", "")).strip(),
                )
            )
            idx += 1
    return paragraphs


def _derive_page_window(pages: Iterable[int], start: int, end: int, context: int) -> List[int]:
    pages = sorted(set(pages))
    if not pages:
        return []
    window_start = max(pages[0], start - max(context, 0))
    window_end = min(pages[-1], end + max(context, 0))
    return [page for page in pages if window_start <= page <= window_end]


def _escape(label: str) -> str:
    return label.replace("\\", "\\\\").replace("\"", "\\\"")


def generate_section_tree_dot(
    docmap: Dict,
    page_start: int,
    page_end: int,
    *,
    context_pages: int = 1,
    text_preview: int = 60,
) -> str:
    """Generate Graphviz DOT text highlighting sections for selected pages.

    Parameters
    ----------
    docmap:
        DocMap-like dictionary output from the pipeline.
    page_start, page_end:
        Inclusive page range of primary interest.
    context_pages:
        Number of pages before and after the range to include for context.
    text_preview:
        Maximum number of characters from each paragraph to show in labels.
    """

    paragraphs = _collect_paragraphs(docmap)
    if not paragraphs:
        return "digraph doc_sections {\n  labelloc=t;\n  label=\"No content\";\n}\n"

    pages_all = [p.page for p in paragraphs]
    window_pages = set(_derive_page_window(pages_all, page_start, page_end, context_pages))
    filtered_paras = [p for p in paragraphs if p.page in window_pages]
    if not filtered_paras:
        return "digraph doc_sections {\n  labelloc=t;\n  label=\"No paragraphs in selected window\";\n}\n"

    # Maps section path to node id
    section_nodes: Dict[Tuple[str, ...], str] = {}
    lines: List[str] = [
        "digraph doc_sections {",
        "  graph [rankdir=LR, fontsize=12, labelloc=t, label=\"DocMap Sections\"];",
        "  node [shape=box, fontname=\"Helvetica\", style=\"filled\", fillcolor=\"#f5f5f5\"];",
    ]

    def get_section_node(path: Tuple[str, ...]) -> str:
        if path in section_nodes:
            return section_nodes[path]
        node_id = f"sec_{len(section_nodes)}"
        label = _escape(path[-1])
        lines.append(f"  {node_id} [label=\"{label}\", shape=folder, fillcolor=\"#e0f7fa\"];\n")
        section_nodes[path] = node_id
        if len(path) > 1:
            parent_node = get_section_node(path[:-1])
            lines.append(f"  {parent_node} -> {node_id};\n")
        else:
            lines.append("  doc_root -> {node_id};\n".replace("{node_id}", node_id))
        return node_id

    lines.append("  doc_root [label=\"Document\", shape=oval, fillcolor=\"#bbdefb\"];\n")

    # Build paragraph nodes grouped by page via subgraphs for readability.
    paras_by_page: Dict[int, List[ParagraphView]] = {}
    for para in filtered_paras:
        paras_by_page.setdefault(para.page, []).append(para)

    for page in sorted(paras_by_page):
        lines.append(f"  subgraph cluster_page_{page} {{\n")
        lines.append(f"    label=\"Page {page}\";\n")
        lines.append("    style=dashed;\n")
        for para in paras_by_page[page]:
            para_id = f"para_{para.idx}"
            text = para.text or "(empty paragraph)"
            if len(text) > text_preview:
                text = text[: text_preview - 1] + "…"
            lines.append(f"    {para_id} [label=\"p{para.page}: {_escape(text)}\", shape=note, fillcolor=\"#fff3e0\"];\n")
            section_node = get_section_node(para.section_path)
            lines.append(f"    {section_node} -> {para_id};\n")
        lines.append("  }\n")

    lines.append("}\n")
    return "".join(lines)


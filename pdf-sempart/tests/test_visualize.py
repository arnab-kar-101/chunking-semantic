from src.pdf_sempart.visualize.docmap_graph import generate_section_tree_dot


def _sample_docmap():
    return {
        "meta": {},
        "sections": [],
        "chunks": [
            {
                "section_path": ["Intro"],
                "topic_node_ids": [],
                "topic_weight": 0.0,
                "paras": [
                    {"page": 1, "text": "Heading", "bbox": [0, 0, 10, 10], "font_size_mean": 14, "bold_ratio": 1.0},
                    {"page": 1, "text": "Body text here", "bbox": [0, 10, 10, 20], "font_size_mean": 12, "bold_ratio": 0.0},
                ],
            },
            {
                "section_path": ["Intro", "Details"],
                "topic_node_ids": [],
                "topic_weight": 0.0,
                "paras": [
                    {"page": 2, "text": "More detail", "bbox": [0, 0, 10, 10], "font_size_mean": 12, "bold_ratio": 0.0},
                ],
            },
        ],
    }


def test_generate_section_tree_dot_includes_sections_and_paras():
    dot = generate_section_tree_dot(_sample_docmap(), 1, 1, context_pages=1)
    assert "Intro" in dot
    assert "Details" in dot
    assert "p1" in dot
    assert "Page 1" in dot


def test_generate_section_tree_dot_handles_empty_window():
    dot = generate_section_tree_dot(_sample_docmap(), 5, 6)
    assert "No paragraphs in selected window" in dot

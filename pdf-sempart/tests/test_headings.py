from types import SimpleNamespace
from src.pdf_sempart.nlp import headings


def test_heading_level_detects_primary_heading():
    paras = [
        SimpleNamespace(text="1. Overview", font_size_mean=20.0),
        SimpleNamespace(text="Body text", font_size_mean=11.0),
        SimpleNamespace(text="More body", font_size_mean=11.0),
        SimpleNamespace(text="Even more body", font_size_mean=11.0),
    ]
    fs_all = [p.font_size_mean for p in paras]
    level = headings.heading_level(paras[0], fs_all)
    assert level == 1

def test_heading_level_non_heading():
    paras = [SimpleNamespace(text="Informational paragraph about results.", font_size_mean=12.0)]
    fs_all = [12.0]
    level = headings.heading_level(paras[0], fs_all)
    assert level == 0

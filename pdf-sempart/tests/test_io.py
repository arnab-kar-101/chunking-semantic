from src.pdf_sempart.io import loaders

def test_load_dict_populates_defaults():
    doc = {
        "text": [{"page": 1, "bbox": [0, 0, 10, 10], "content": "Hello"}],
        "table": [{"page": 1, "bbox": [0, 0, 5, 5], "content": "tbl"}],
        "image": []
    }
    normalized = loaders.load_dict(doc)
    assert normalized["text"][0]["font_size"] == 12
    assert normalized["text"][0]["is_bold"] is False

def test_to_blocks_converts_all_modalities():
    doc = {
        "text": [{"page": 1, "bbox": [0, 0, 10, 10], "content": "Hello", "font_size": 11, "is_bold": True}],
        "table": [{"page": 2, "bbox": [1, 1, 5, 5], "content": "tbl"}],
        "image": [{"page": 3, "bbox": [2, 2, 4, 4], "content": "img"}]
    }
    blocks = loaders.to_blocks(doc)
    kinds = {b.kind for b in blocks}
    assert kinds == {"text", "table", "image"}
    assert blocks[0].font_size == 11
    assert blocks[0].is_bold is True

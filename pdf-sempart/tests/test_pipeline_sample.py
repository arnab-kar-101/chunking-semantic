import json
from pathlib import Path
from unittest import mock

from src.pdf_sempart.pipeline import run
from src.pdf_sempart.layout import merge as merge_module

ORIGINAL_MERGE = merge_module.merge_blocks_to_paras

SAMPLE_PATH = Path(__file__).resolve().parents[1] / "examples" / "sample.json"


def _load_sample_doc():
    raw = json.loads(SAMPLE_PATH.read_text())
    doc = {"text": [], "table": [], "image": []}
    for entry in raw:
        category = entry.get("category", "text").lower()
        font_size = 18 if "header" in category else 12
        is_bold = "header" in category
        doc["text"].append({
            "page": 1,
            "bbox": entry["bbox"],
            "content": entry["text"],
            "font_size": font_size,
            "is_bold": is_bold,
        })
    return doc


def _config():
    return {
        "models": {"embed_a": "stub-a", "embed_b": "stub-b"},
        "merge": {"gap_px_thresh": 60.0, "cos_join": 0.5},
        "hlda": {"depth": 3, "alpha": 1.0, "gamma": 1.0, "eta": 0.1, "min_cf": 1, "iters": 5, "burn_in": 1},
        "boundaries": {"cos_thresh": 1.1, "hell_thresh": 0.0},
    }


class StubEncoder:
    def __init__(self, model_id):
        self.model_id = model_id

    def encode(self, texts):
        return [[float(len(t.split()))] for t in texts]


class StubHLDA:
    def __init__(self, **kwargs):
        self.depth = kwargs.get("depth", 3)

    def fit(self, docs_tokens):
        # No-op for deterministic tests
        self._seen = docs_tokens

    def infer(self, tokens):
        base = 1.0 / self.depth
        return list(range(self.depth)), [base] * self.depth


def test_process_document_with_sample_json():
    doc = _load_sample_doc()
    cfg = _config()
    captured = {}

    def spy_merge(blocks, encA, gap_px_thresh, cos_join):
        result = ORIGINAL_MERGE(blocks, encA, gap_px_thresh, cos_join)
        captured["paras"] = result
        return result

    def boundary_stub(topic_dists, embA, embB, cos_thresh, hell_thresh):
        texts = [p.text for p in captured.get("paras", [])]
        boundaries = [False] * len(topic_dists)
        for i, text in enumerate(texts):
            if "Investors and others should note" in text or text.startswith("The information we post"):
                boundaries[i] = True
        return boundaries

    with mock.patch.object(run.encoder_a, "Encoder", StubEncoder), \
         mock.patch.object(run.encoder_b, "Encoder", StubEncoder), \
         mock.patch.object(run.hlda, "HLDA", StubHLDA), \
         mock.patch.object(run.merge, "merge_blocks_to_paras", spy_merge), \
         mock.patch.object(run.voter, "detect_boundaries", side_effect=boundary_stub):
        docmap = run.process_document(doc, cfg)

    assert docmap.meta["model_ids"] == ["stub-a", "stub-b"]
    assert len(docmap.chunks) == 3

    first_chunk_texts = [para["text"] for para in docmap.chunks[0]["paras"]]
    assert first_chunk_texts[0] == "Table of Contents"
    assert any("Forward-Looking" in text for text in first_chunk_texts)

    second_chunk = docmap.chunks[1]
    assert second_chunk["paras"][0]["text"].startswith("Investors and others should note")
    assert second_chunk["section_path"][0].startswith("## Forward-Looking Statements")

    final_chunk = docmap.chunks[2]
    assert final_chunk["paras"][0]["text"].startswith("The information we post through these social media channels")
    assert final_chunk["paras"][-1]["text"] == "3"

import json
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from src.pdf_sempart.pipeline import run

TEST_DATA = Path(__file__).parent / "data" / "sample_report.json"


class StubEncoder:
    def __init__(self, model_id):
        self.model_id = model_id

    def encode(self, texts):
        return [[float(len(t.split()))] for t in texts]


class StubHLDA:
    def __init__(self, **kwargs):
        self.depth = kwargs.get("depth", 2)
        self.seen = []

    def fit(self, docs_tokens):
        self.seen = docs_tokens

    def infer(self, tokens):
        path = list(range(self.depth))
        dist = [1.0 / self.depth] * self.depth
        return path, dist


def _config():
    return {
        "models": {"embed_a": "stub-a", "embed_b": "stub-b"},
        "merge": {"gap_px_thresh": 40.0, "cos_join": 0.5},
        "hlda": {"depth": 2, "alpha": 1.0, "gamma": 1.0, "eta": 0.1, "min_cf": 1, "iters": 10, "burn_in": 2},
        "boundaries": {"cos_thresh": 1.1, "hell_thresh": 0.0},
    }


def test_process_document_stubbed_end_to_end():
    doc = json.loads(TEST_DATA.read_text())
    cfg = _config()
    with mock.patch.object(run.encoder_a, "Encoder", StubEncoder), \
         mock.patch.object(run.encoder_b, "Encoder", StubEncoder), \
         mock.patch.object(run.hlda, "HLDA", StubHLDA), \
         mock.patch.object(run.voter, "detect_boundaries", return_value=[False, True, False, False]):
        docmap = run.process_document(doc, cfg)

    assert docmap.meta["model_ids"] == ["stub-a", "stub-b"]
    assert len(docmap.chunks) == 2
    first_chunk = docmap.chunks[0]
    assert first_chunk["section_path"][0].startswith("1. Overview")
    assert len(first_chunk["paras"]) == 1
    assert docmap.chunks[1]["section_path"][0].startswith("1. Overview")

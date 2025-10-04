import os


class Encoder:
    def __init__(self, model_id):
        self.model_id = model_id
        self._model = None
        self._use_stub = os.getenv("PDF_SEMPART_USE_STUB_ENCODERS", "").lower() in ("1", "true", "yes")

    def _ensure_model(self):
        if self._model is not None:
            return
        if self._use_stub:
            class _StubModel:
                def encode(self, texts, normalize_embeddings=True):
                    return [[float(len(t.split()))] for t in texts]

            self._model = _StubModel()
            return
        from sentence_transformers import SentenceTransformer

        self._model = SentenceTransformer(self.model_id, device='cpu')

    def encode(self, texts):
        self._ensure_model()
        arr = self._model.encode(texts, normalize_embeddings=True)
        return [list(vec) for vec in arr]

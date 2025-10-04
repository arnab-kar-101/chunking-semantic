class Encoder:
    def __init__(self, model_id):
        self.model_id = model_id
        self._model = None

    def _ensure_model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_id, device='cpu')

    def encode(self, texts):
        self._ensure_model()
        arr = self._model.encode(texts, normalize_embeddings=True)
        return [list(vec) for vec in arr]

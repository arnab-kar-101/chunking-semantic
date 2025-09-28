from sentence_transformers import SentenceTransformer
import numpy as np

class Encoder:
    def __init__(self, model_id):
        self.model = SentenceTransformer(model_id, device='cpu')
    def encode(self, texts):
        arr = self.model.encode(texts, normalize_embeddings=True)
        return np.array(arr)

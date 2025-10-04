import importlib
import math
import os
from collections import Counter


_BACKEND = os.getenv("PDF_SEMPART_TOPIC_BACKEND", "stub").lower()
_TP_MODULE = None
if _BACKEND == "tomotopy":
    _TP_MODULE = importlib.import_module("tomotopy")


class HLDA:
    """Configurable HLDA wrapper that falls back to a lightweight stub."""

    def __init__(self, depth, alpha, gamma, eta, min_cf, iters, burn_in):
        self.depth = max(1, depth)
        self._backend = "tomotopy" if _TP_MODULE else "stub"
        if self._backend == "tomotopy":
            self._model = _TP_MODULE.HLDAModel(depth=self.depth, alpha=alpha, gamma=gamma, eta=eta, min_cf=min_cf)
            self._model.burn_in = burn_in
            self._iters = iters
        else:
            self._vocab = Counter()

    def fit(self, docs_tokens):
        if self._backend == "tomotopy":
            for tokens in docs_tokens:
                self._model.add_doc(tokens)
            self._model.train(self._iters)
        else:
            for doc in docs_tokens:
                self._vocab.update(token for token in doc if token)

    def infer(self, tokens):
        if self._backend == "tomotopy":
            doc = self._model.make_doc(tokens)
            self._model.infer(doc, iter=200)
            path = list(doc.levels)
            base = 1.0 / self.depth
            dist = [base] * self.depth
            norm = math.sqrt(sum(d * d for d in dist)) or 1.0
            return path, [d / norm for d in dist]

        counts = Counter(token for token in tokens if token)
        path = [idx for idx in range(self.depth)]
        base = 1.0 / self.depth
        dist = [base] * self.depth
        if counts:
            total = sum(counts.values()) or 1
            boost = min(0.5, counts.most_common(1)[0][1] / total)
            dist[0] = base + boost
            remainder = (1.0 - dist[0]) / max(1, self.depth - 1)
            for i in range(1, self.depth):
                dist[i] = remainder
        norm = math.sqrt(sum(d * d for d in dist)) or 1.0
        return path, [d / norm for d in dist]

import tomotopy as tp
import numpy as np

class HLDA:
    def __init__(self, depth, alpha, gamma, eta, min_cf, iters, burn_in):
        self.depth = depth
        self.alpha = alpha
        self.gamma = gamma
        self.eta = eta
        self.min_cf = min_cf
        self.iters = iters
        self.burn_in = burn_in
        self.mdl = None

    def fit(self, docs_tokens):
        mdl = tp.HLDAModel(depth=self.depth, alpha=self.alpha, gamma=self.gamma, eta=self.eta, min_cf=self.min_cf)
        for t in docs_tokens:
            mdl.add_doc(t)
        mdl.burn_in = self.burn_in
        mdl.train(self.iters)
        self.mdl = mdl

    def infer(self, tokens):
        d = self.mdl.make_doc(tokens)
        self.mdl.infer(d, iter=200)
        path = list(d.levels)
        k = self.depth
        dist = np.zeros(k)
        for i, nid in enumerate(path):
            dist[i] = 1.0 / k
        dist = dist / (np.linalg.norm(dist) + 1e-8)
        return path, dist

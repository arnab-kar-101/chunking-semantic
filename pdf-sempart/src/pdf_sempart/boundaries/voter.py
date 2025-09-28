import numpy as np
from scipy.spatial.distance import cosine

def hellinger(p, q):
    p = np.asarray(p)
    q = np.asarray(q)
    return np.sqrt(0.5 * np.sum((np.sqrt(p) - np.sqrt(q)) ** 2))

def detect_boundaries(topic_dists, embA, embB, cos_thresh, hell_thresh):
    N = len(topic_dists)
    boundaries = [False] * N
    for i in range(2, N):
        T1 = hellinger(topic_dists[i], topic_dists[i-1]) >= hell_thresh
        T2 = hellinger(topic_dists[i], topic_dists[i-2]) >= hell_thresh
        E1 = cosine(embA[i], embA[i-1]) < cos_thresh
        E2 = cosine(embB[i], embB[i-1]) < cos_thresh
        if T1 and T2 and E1 and E2:
            boundaries[i] = True
    return boundaries

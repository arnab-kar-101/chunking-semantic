import math


def _hellinger(p, q):
    total = 0.0
    for a, b in zip(p, q):
        total += (math.sqrt(max(a, 0.0)) - math.sqrt(max(b, 0.0))) ** 2
    return math.sqrt(0.5 * total)


def _cosine_distance(a, b):
    dot = sum(float(x) * float(y) for x, y in zip(a, b))
    norm_a = math.sqrt(sum(float(x) ** 2 for x in a))
    norm_b = math.sqrt(sum(float(x) ** 2 for x in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 1.0
    cosine_sim = dot / (norm_a * norm_b)
    return 1.0 - cosine_sim


def detect_boundaries(topic_dists, embA, embB, cos_thresh, hell_thresh):
    N = len(topic_dists)
    boundaries = [False] * N
    for i in range(2, N):
        T1 = _hellinger(topic_dists[i], topic_dists[i-1]) >= hell_thresh
        T2 = _hellinger(topic_dists[i], topic_dists[i-2]) >= hell_thresh
        E1 = _cosine_distance(embA[i], embA[i-1]) < cos_thresh
        E2 = _cosine_distance(embB[i], embB[i-1]) < cos_thresh
        if T1 and T2 and E1 and E2:
            boundaries[i] = True
    return boundaries

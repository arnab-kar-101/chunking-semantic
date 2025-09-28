import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict

def assign_columns(blocks, max_k=3):
    xs = np.array([(b.bbox[0] + b.bbox[2]) / 2 for b in blocks]).reshape(-1, 1)
    best_k, best_inertia, best_labels = 1, float('inf'), None
    for k in range(1, max_k + 1):
        kmeans = KMeans(n_clusters=k, n_init=10, random_state=42).fit(xs)
        if kmeans.inertia_ < best_inertia:
            best_k, best_inertia, best_labels = k, kmeans.inertia_, kmeans.labels_
    # Remap labels by center x ascending
    centers = [np.mean(xs[best_labels == i]) for i in range(best_k)]
    order = np.argsort(centers)
    col_id_map = {i: int(order[i]) for i in range(best_k)}
    col_ids = [col_id_map[l] for l in best_labels]
    for b, cid in zip(blocks, col_ids):
        b.col_id = cid
    return blocks

def reading_order(blocks):
    by_page = defaultdict(list)
    for b in blocks:
        by_page[b.page].append(b)
    ordered = []
    for page in sorted(by_page):
        page_blocks = assign_columns(by_page[page])
        page_blocks.sort(key=lambda b: (b.col_id, b.bbox[1], b.bbox[0]))
        ordered.extend(page_blocks)
    return ordered

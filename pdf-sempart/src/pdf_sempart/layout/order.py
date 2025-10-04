from collections import defaultdict


def _column_assignments(blocks, max_k):
    if not blocks:
        return {}
    centers = [((b.bbox[0] + b.bbox[2]) / 2.0, b) for b in blocks]
    centers.sort(key=lambda item: item[0])

    xs = [c for c, _ in centers]
    min_x, max_x = min(xs), max(xs)
    span = max(max_x - min_x, 1.0)
    base_gap = span / float(max(1, max_k))
    gap_threshold = max(40.0, base_gap * 0.5)

    assignments = {}
    current_col = 0
    prev_x = xs[0]
    for x, block in centers:
        if current_col < max_k - 1 and (x - prev_x) > gap_threshold:
            current_col += 1
        assignments[id(block)] = current_col
        prev_x = x
    return assignments


def assign_columns(blocks, max_k=3):
    assignments = _column_assignments(blocks, max_k)
    for b in blocks:
        b.col_id = assignments.get(id(b), 0)
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

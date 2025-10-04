from ..layout.order import reading_order
from typing import List
from ..layout.blocks import Block


def _mean(values, default):
    return float(sum(values) / len(values)) if values else float(default)


def _dot(a, b):
    return sum(float(x) * float(y) for x, y in zip(a, b))


def merge_blocks_to_paras(blocks: List[Block], encA, gap_px_thresh: float, cos_join: float):
    blocks = reading_order(blocks)
    paras, cur = [], []
    prev_col, prev_page, prev_y1 = None, None, None
    for b in blocks:
        hard_break = False
        if not cur:
            cur.append(b)
            prev_col, prev_page, prev_y1 = getattr(b, 'col_id', 0), b.page, b.bbox[3]
            continue
        col, page, y0 = getattr(b, 'col_id', 0), b.page, b.bbox[1]
        vertical_gap = y0 - prev_y1 if page == prev_page and col == prev_col else float('inf')
        if page != prev_page or col != prev_col or vertical_gap > gap_px_thresh:
            hard_break = True
        else:
            prev_text = ' '.join(x.content for x in cur)
            e_prev = encA.encode([prev_text])[0]
            e_curr = encA.encode([b.content])[0]
            ends_sentence = prev_text.strip().endswith(('.', '!', '?'))
            if ends_sentence and _dot(e_prev, e_curr) < cos_join:
                hard_break = True
        if hard_break:
            paras.append(cur)
            cur = [b]
        else:
            cur.append(b)
        prev_col, prev_page, prev_y1 = col, page, b.bbox[3]
    if cur:
        paras.append(cur)
    # Compute paragraph features
    para_objs = []
    for para in paras:
        texts = [b.content for b in para]
        bbox = [
            min(b.bbox[0] for b in para),
            min(b.bbox[1] for b in para),
            max(b.bbox[2] for b in para),
            max(b.bbox[3] for b in para)
        ]
        font_sizes = [b.font_size for b in para if b.kind == 'text' and b.font_size]
        bolds = [b.is_bold for b in para if b.kind == 'text']
        font_size_mean = _mean(font_sizes, 12.0)
        bold_ratio = _mean(bolds, 0.0)
        para_objs.append(type('Para', (), {
            'text': ' '.join(texts),
            'bbox': bbox,
            'page': para[0].page,
            'font_size_mean': font_size_mean,
            'bold_ratio': bold_ratio,
            'blocks': para
        }))
    return para_objs

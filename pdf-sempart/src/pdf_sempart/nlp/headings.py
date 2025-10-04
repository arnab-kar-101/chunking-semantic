import re
from statistics import mean, pstdev


def _stats(values):
    if not values:
        return 0.0, 0.0
    avg = mean(values)
    std = pstdev(values) if len(values) > 1 else 0.0
    return avg, std


def heading_level(para, fs_all):
    text = para.text.strip()
    is_short = len(text) < 120
    avg, std = _stats(fs_all)
    denom = std if std > 0 else 1e-6
    fs_z = (para.font_size_mean - avg) / denom
    numbered = re.match(r'^\d+(\.\d+)*\s+', text)
    all_caps = re.match(r'^[A-Z0-9][A-Z0-9 \-:]+$', text)
    if is_short and fs_z > 1.5:
        return 1
    if is_short and (fs_z > 0.6) and (numbered or all_caps):
        return 2
    if is_short and (numbered or all_caps):
        return 3
    return 0

import re
import numpy as np

def heading_level(para, fs_all):
    text = para.text.strip()
    is_short = len(text) < 120
    fs_z = (para.font_size_mean - np.mean(fs_all)) / (np.std(fs_all) + 1e-6)
    numbered = re.match(r'^\d+(\.\d+)*\s+', text)
    all_caps = re.match(r'^[A-Z0-9][A-Z0-9 \-:]+$', text)
    if is_short and fs_z > 1.5:
        return 1
    if is_short and (fs_z > 0.6) and (numbered or all_caps):
        return 2
    if is_short and (numbered or all_caps):
        return 3
    return 0

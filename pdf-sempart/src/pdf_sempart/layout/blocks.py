from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Block:
    kind: str  # 'text', 'table', 'image'
    page: int
    bbox: List[float]  # [x0, y0, x1, y1]
    content: str
    font_size: Optional[float] = None
    is_bold: Optional[bool] = False

from typing import Dict, List, Any
from ..layout.blocks import Block

def load_dict(input_obj: dict) -> Dict:
    assert all(k in input_obj for k in ('text', 'table', 'image'))
    for kind in ('text', 'table', 'image'):
        for item in input_obj[kind]:
            assert 'page' in item and 'bbox' in item and 'content' in item
            if kind == 'text':
                item.setdefault('font_size', 12)
                item.setdefault('is_bold', False)
    return input_obj

def to_blocks(doc: Dict) -> List[Block]:
    blocks = []
    for kind in ('text', 'table', 'image'):
        for item in doc[kind]:
            blocks.append(Block(
                kind=kind,
                page=item['page'],
                bbox=item['bbox'],
                content=item['content'],
                font_size=item.get('font_size'),
                is_bold=item.get('is_bold', False)
            ))
    return blocks

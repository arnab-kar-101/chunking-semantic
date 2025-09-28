from dataclasses import dataclass, field
from typing import List, Dict, Any
import datetime
import json

@dataclass
class Chunk:
    section_path: List[str]
    topic_node_ids: List[int]
    topic_weight: float
    paras: List[Dict[str, Any]]  # page, text, bbox, font_size_mean, bold_ratio

@dataclass
class SectionNode:
    title: str
    level: int
    start_idx: int
    children: List[Any] = field(default_factory=list)

@dataclass
class DocMap:
    meta: Dict[str, Any]
    sections: List[SectionNode]
    chunks: List[Chunk]

def build_docmap(meta, sections, chunks):
    return DocMap(meta=meta, sections=sections, chunks=chunks)

def validate_docmap(docmap: DocMap) -> None:
    assert hasattr(docmap, 'meta')
    assert hasattr(docmap, 'sections')
    assert hasattr(docmap, 'chunks')
    # Add more validation as needed

# For JSON serialization
class DocMapEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return super().default(obj)

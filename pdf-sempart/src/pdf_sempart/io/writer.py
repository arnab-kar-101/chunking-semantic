import json
from .schema import DocMapEncoder

def save_json(docmap, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(docmap, f, cls=DocMapEncoder, indent=2, ensure_ascii=False)

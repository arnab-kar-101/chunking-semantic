import argparse
import yaml
import json
from ..pipeline import run
from ..io import loaders

def main():
    parser = argparse.ArgumentParser(description="PDF Semantic Chunking with hLDA and dual embeddings.")
    parser.add_argument('--in', dest='input_path', required=True, help='Input JSON file (from dots.ocr)')
    parser.add_argument('--out', dest='output_path', required=True, help='Output DocMap JSON file')
    parser.add_argument('--config', dest='config_path', default='config/defaults.yaml', help='YAML config file')
    args = parser.parse_args()

    with open(args.config_path, 'r') as f:
        cfg = yaml.safe_load(f)
    with open(args.input_path, 'r') as f:
        doc_dict = json.load(f)
    doc_dict = loaders.load_dict(doc_dict)
    docmap = run.process_document(doc_dict, cfg, args.output_path)
    print(f"DocMap written to {args.output_path}")
    print(f"Sections: {len(docmap.sections) if hasattr(docmap, 'sections') else 'N/A'} | Chunks: {len(docmap.chunks) if hasattr(docmap, 'chunks') else 'N/A'}")

if __name__ == '__main__':
    main()

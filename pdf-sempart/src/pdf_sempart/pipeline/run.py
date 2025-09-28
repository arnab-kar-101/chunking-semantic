import numpy as np
from ..io import loaders, writer, schema
from ..layout import merge
from ..embed import encoder_a, encoder_b
from ..nlp import preprocess, headings
from ..topics import hlda
from ..boundaries import voter
from ..sectionize import build
import datetime

def process_document(doc_dict, cfg, output_path=None):
    # Load blocks
    blocks = loaders.to_blocks(doc_dict)
    # Merge to paragraphs
    encA = encoder_a.Encoder(cfg['models']['embed_a'])
    paras = merge.merge_blocks_to_paras(blocks, encA, cfg['merge']['gap_px_thresh'], cfg['merge']['cos_join'])
    # Embeddings
    encB = encoder_b.Encoder(cfg['models']['embed_b'])
    texts = [p.text for p in paras]
    embA = encA.encode(texts)
    embB = encB.encode(texts)
    for i, p in enumerate(paras):
        p.embA = embA[i]
        p.embB = embB[i]
    # Tokens and topics
    tokens = [preprocess.tokens_for(t) for t in texts]
    hlda_model = hlda.HLDA(**cfg['hlda'])
    hlda_model.fit(tokens)
    topic_paths, topic_dists = [], []
    for toks in tokens:
        path, dist = hlda_model.infer(toks)
        topic_paths.append(path)
        topic_dists.append(dist)
    # 3-way voting
    boundaries = voter.detect_boundaries(topic_dists, embA, embB, cfg['boundaries']['cos_thresh'], cfg['boundaries']['hell_thresh'])
    # Headings + sections
    fs_all = np.array([p.font_size_mean for p in paras])
    levels = [headings.heading_level(p, fs_all) for p in paras]
    tree = build.assemble_tree(paras, boundaries, levels)
    # Build chunks
    chunks = []
    current, current_path = [], []
    for i, p in enumerate(paras):
        if i > 0 and boundaries[i]:
            chunks.append(make_chunk(current, current_path, tree, paras))
            current, current_path = [], []
        current.append(p)
        if topic_paths[i]:
            current_path = topic_paths[i]
    if current:
        chunks.append(make_chunk(current, current_path, tree, paras))
    # DocMap
    meta = {
        'hlda_depth': cfg['hlda']['depth'],
        'cos_thresh': cfg['boundaries']['cos_thresh'],
        'hell_thresh': cfg['boundaries']['hell_thresh'],
        'model_ids': [cfg['models']['embed_a'], cfg['models']['embed_b']],
        'created_at': datetime.datetime.now().isoformat()
    }
    docmap = schema.build_docmap(meta, tree, chunks)
    if output_path:
        writer.save_json(docmap, output_path)
    return docmap

def make_chunk(current_paras, path_ids, tree, all_paras):
    avg_emb = np.mean([p.embA for p in current_paras], axis=0)
    weight = float(np.linalg.norm(avg_emb))
    section_path = build.derive_section_path(all_paras, tree, current_paras)
    return {
        'section_path': section_path,
        'topic_node_ids': path_ids,
        'topic_weight': weight,
        'paras': [
            {
                'page': p.page,
                'text': p.text,
                'bbox': p.bbox,
                'font_size_mean': p.font_size_mean,
                'bold_ratio': p.bold_ratio
            } for p in current_paras
        ]
    }

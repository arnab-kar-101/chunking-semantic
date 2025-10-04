import datetime
import math
from ..io import loaders, writer, schema
from ..layout import merge
from ..embed import encoder_a, encoder_b
from ..nlp import preprocess, headings
from ..topics import hlda
from ..boundaries import voter
from ..sectionize import build


def _vectorize(sequence):
    result = []
    for item in sequence:
        if hasattr(item, 'tolist'):
            result.append(list(item.tolist()))
        elif isinstance(item, (list, tuple)):
            result.append([float(x) for x in item])
        else:
            result.append([float(item)])
    return result


def _vector_mean(vectors):
    if not vectors:
        return []
    length = len(vectors[0])
    totals = [0.0] * length
    for vec in vectors:
        for idx in range(length):
            totals[idx] += float(vec[idx])
    count = float(len(vectors))
    return [val / count for val in totals]


def _vector_norm(vec):
    return math.sqrt(sum(float(x) ** 2 for x in vec))

def process_document(doc_dict, cfg, output_path=None):
    # Load blocks
    blocks = loaders.to_blocks(doc_dict)
    # Merge to paragraphs
    encA = encoder_a.Encoder(cfg['models']['embed_a'])
    paras = merge.merge_blocks_to_paras(blocks, encA, cfg['merge']['gap_px_thresh'], cfg['merge']['cos_join'])
    # Embeddings
    encB = encoder_b.Encoder(cfg['models']['embed_b'])
    texts = [p.text for p in paras]
    embA = _vectorize(encA.encode(texts))
    embB = _vectorize(encB.encode(texts))
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
    fs_all = [p.font_size_mean for p in paras]
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
    avg_emb = _vector_mean([p.embA for p in current_paras])
    weight = float(_vector_norm(avg_emb))
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

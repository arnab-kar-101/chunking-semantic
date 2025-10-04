from src.pdf_sempart.boundaries.voter import detect_boundaries

def test_detect_boundaries():
    topic_dists = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    embA = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    embB = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    boundaries = detect_boundaries(topic_dists, embA, embB, cos_thresh=1.1, hell_thresh=0.35)
    assert boundaries[2] == True

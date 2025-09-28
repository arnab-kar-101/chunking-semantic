from src.pdf_sempart.boundaries.voter import detect_boundaries
import numpy as np

def test_detect_boundaries():
    topic_dists = [np.array([1,0,0]), np.array([0,1,0]), np.array([0,0,1])]
    embA = np.eye(3)
    embB = np.eye(3)
    boundaries = detect_boundaries(topic_dists, embA, embB, cos_thresh=0.7, hell_thresh=0.35)
    assert boundaries[2] == True

from src.pdf_sempart.topics.hlda import HLDA

def test_hlda_fit_infer():
    docs = [['hello', 'world'], ['another', 'topic']]
    model = HLDA(depth=2, alpha=10.0, gamma=1.0, eta=0.1, min_cf=1, iters=10, burn_in=2)
    model.fit(docs)
    path, dist = model.infer(['hello', 'world'])
    assert len(path) == 2
    assert dist.shape[0] == 2

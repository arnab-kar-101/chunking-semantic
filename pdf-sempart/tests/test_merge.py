# Test for merge_blocks_to_paras: sentence end + low cosine triggers split
# (Mock encoder for cosine)
from src.pdf_sempart.layout.merge import merge_blocks_to_paras
from src.pdf_sempart.layout.blocks import Block
class DummyEncoder:
    def encode(self, texts):
        # Return 1.0 for first, 0.0 for second to force low cosine
        return [[1.0], [0.0]] if len(texts) == 2 else [[1.0]]
def test_merge_blocks_to_paras():
    blocks = [
        Block(kind='text', page=1, bbox=[0,0,10,10], content='Hello world.'),
        Block(kind='text', page=1, bbox=[0,20,10,30], content='Next para.')
    ]
    paras = merge_blocks_to_paras(blocks, DummyEncoder(), 16.0, 0.72)
    assert len(paras) == 2

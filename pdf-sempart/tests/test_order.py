from src.pdf_sempart.layout.order import reading_order
from src.pdf_sempart.layout.blocks import Block

def test_reading_order():
    blocks = [
        Block(kind='text', page=1, bbox=[100, 100, 200, 120], content='A'),
        Block(kind='text', page=1, bbox=[300, 100, 400, 120], content='B'),
        Block(kind='text', page=1, bbox=[100, 200, 200, 220], content='C'),
        Block(kind='text', page=1, bbox=[300, 200, 400, 220], content='D'),
    ]
    ordered = reading_order(blocks)
    assert ordered[0].content == 'A'
    assert ordered[1].content == 'C'
    assert ordered[2].content == 'B'
    assert ordered[3].content == 'D'

from src.pdf_sempart.sectionize.build import assemble_tree
class Para:
    def __init__(self, text, font_size_mean):
        self.text = text
        self.font_size_mean = font_size_mean

def test_assemble_tree():
    paras = [Para('1. Introduction', 16), Para('Background', 14), Para('Details', 12)]
    boundaries = [True, False, False]
    levels = [1, 2, 0]
    tree = assemble_tree(paras, boundaries, levels)
    assert tree[0]['title'].startswith('1. Introduction')
    assert tree[0]['children'][0]['title'] == 'Background'

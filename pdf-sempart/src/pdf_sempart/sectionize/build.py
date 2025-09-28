def assemble_tree(paras, boundaries, levels):
    tree, stack = [], []
    for i, p in enumerate(paras):
        lvl = levels[i]
        if boundaries[i] or lvl > 0:
            if lvl == 0:
                lvl = 2
            while len(stack) >= lvl:
                stack.pop()
            node = {
                'title': p.text[:120],
                'level': lvl,
                'start_idx': i,
                'children': []
            }
            if not stack:
                tree.append(node)
            else:
                stack[-1]['children'].append(node)
            stack.append(node)
    return tree

def derive_section_path(paras, tree, span_paras):
    target_idx = paras.index(span_paras[0])
    best = ["", "", ""]
    def dfs(node, cur):
        if node['start_idx'] <= target_idx:
            cur2 = cur.copy()
            cur2[node['level']-1] = node['title']
            for child in node['children']:
                dfs(child, cur2)
            nonlocal best
            if sum(1 for x in cur2 if x) > sum(1 for x in best if x):
                best = cur2
    for node in tree:
        dfs(node, ["", "", ""])
    return best

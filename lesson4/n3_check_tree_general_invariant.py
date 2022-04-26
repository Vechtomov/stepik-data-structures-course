import sys


class Node:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right


def check_invariant(node: Node, min_val, max_val):
    if node is None:
        return True
    if max_val is not None and node.key >= max_val:
        return False
    if min_val is not None and node.key < min_val:
        return False
    return check_invariant(node.left, min_val, node.key) and check_invariant(node.right, node.key, max_val)


def build_tree(commands):
    nodes = [Node(0) for _ in range(len(commands))]
    for i, (k, l, r) in enumerate(commands):
        nodes[i].key = k
        if l != -1:
            nodes[i].left = nodes[l]
        if r != -1:
            nodes[i].right = nodes[r]
    return nodes[0]


def solve(commands):
    if len(commands) == 0:
        is_correct = True
    else:
        root = build_tree(commands)
        is_correct = check_invariant(root, None, None)
    print('CORRECT' if is_correct else 'INCORRECT')


def main():
    reader = (s for s in sys.stdin)
    n = int(next(reader))
    commands = [list(map(int, next(reader).split())) for _ in range(n)]
    solve(commands)


if __name__ == "__main__":
    main()

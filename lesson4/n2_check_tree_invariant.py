import sys


class Node:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right


def in_order_no_recursion(root: Node):
    st = []
    curr = root
    while curr is not None or len(st) > 0:
        if curr is not None:
            st.append(curr)
            curr = curr.left
        else:
            curr = st.pop()
            yield curr.key
            curr = curr.right


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
        l = list(in_order_no_recursion(root))
        is_correct = all(l[i] <= l[i+1] for i in range(len(l) - 1))
    print('CORRECT' if is_correct else 'INCORRECT')


def main():
    reader = (s for s in sys.stdin)
    n = int(next(reader))
    commands = [list(map(int, next(reader).split())) for _ in range(n)]
    solve(commands)


if __name__ == "__main__":
    main()

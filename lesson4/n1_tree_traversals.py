import sys

class Node:
    def __init__(self, key, left = None, right = None):
        self.key = key
        self.left = left
        self.right = right

def in_order(node: Node):
    if node is None:
        return
    for k in in_order(node.left):
        yield k
    yield node.key
    for k in in_order(node.right):
        yield k

def pre_order(node: Node):
    if node is None:
        return
    yield node.key
    for k in pre_order(node.left):
        yield k
    for k in pre_order(node.right):
        yield k
        
def post_order(node: Node):
    if node is None:
        return
    for k in post_order(node.left):
        yield k
    for k in post_order(node.right):
        yield k
    yield node.key

def solve(commands):
    nodes = [Node(0) for _ in range(len(commands))]
    for i, (k, l, r) in enumerate(commands):
        nodes[i].key = k
        if l != -1:
            nodes[i].left = nodes[l]
        if r != -1:
            nodes[i].right = nodes[r]
    root = nodes[0]
    print(" ".join(map(str, in_order(root))))
    print(" ".join(map(str, pre_order(root))))
    print(" ".join(map(str, post_order(root))))

def main():
    reader = (s for s in sys.stdin)
    n = int(next(reader))
    commands = [list(map(int, next(reader).split())) for _ in range(n)]
    solve(commands)

if __name__ == "__main__":
    main()
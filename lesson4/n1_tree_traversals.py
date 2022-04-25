import sys

class Node:
    def __init__(self, key, left = None, right = None):
        self.key = key
        self.left = left
        self.rigth = right

def in_order(node: Node):
    if node is None:
        return
    for k in in_order(node.left):
        yield k
    yield node.key
    for k in in_order(node.rigth):
        yield k

def solve(commands):
    left = Node(1)
    right = Node(3)
    root = Node(2, left, right)
    print(" ".join(map(str, in_order(root))))

def main():
    reader = (s for s in sys.stdin)
    n = int(next(reader))
    commands = [list(map(int, next(reader).split())) for _ in range(n)]
    solve(commands)

if __name__ == "__main__":
    main()
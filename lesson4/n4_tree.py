import sys
from __future__ import annotations

class Node:
    def __init__(self, k, l=None, r=None, p=None):
        self.k: int = k
        self.l: Node = l
        self.r: Node = r
        self.p: Node = p
        self.lh: int = 0
        self.rh: int = 0
        self.ls: int = 0
        self.rs: int = 0

def calc_height_all(node: Node):
    cur = node
    while cur.p is not None:
        calc_height_parent(node)
        cur = cur.p

def calc_height_parent(node: Node):
    if node.p is None:
        return
    if node.k < node.p.k:
        node.p.lh = max(node.lh, node.rh) + 1
    else:
        node.p.rh = max(node.lh, node.rh) + 1

def repair_invariant(node: Node):
    if abs(node.lh - node.rh) <= 1:
        return node
    b = node
    a = b.l
    c = b.r
    root = b
    if b.lh > b.rh:
        if a.lh > a.rh:
            root = a
            b.l = a.r
            a.r = b
        else:
            pass
    else:
        pass
    return root
    

class Tree:
    def __init__(self) -> None:
        self.root = None

    def add(self, k):
        if self.root is None:
            self.root = Node(k)
        else:
            self._add(self.root, Node(k))

    def _add(self, node: Node, new_node: Node):
        if node.k > new_node.k:
            if node.l is None:
                node.l = new_node
                new_node.p = node
                calc_height_parent(new_node)
            else:
                self._add(node.l, new_node)
        else:
            if node.r is None:
                node.r = new_node
                new_node.p = node
                calc_height_parent(new_node)
            else:
                self._add(node.r, new_node)
        return new_node

    


def check_invariant_no_recursion(root: Node):
    st = [(root, None, None)]
    while len(st) > 0:
        node, min_val, max_val = st.pop()
        if node is None:
            continue
        if max_val is not None and node.k >= max_val:
            return False
        if min_val is not None and node.k < min_val:
            return False
        st.append((node.l, min_val, node.k))
        st.append((node.r, node.k, max_val))
    return True


def check_invariant(node: Node, min_val, max_val):
    if node is None:
        return True
    if max_val is not None and node.k >= max_val:
        return False
    if min_val is not None and node.k < min_val:
        return False
    return check_invariant(node.l, min_val, node.k) and check_invariant(node.r, node.k, max_val)


def build_tree(commands):
    nodes = [Node(0) for _ in range(len(commands))]
    for i, (k, l, r) in enumerate(commands):
        nodes[i].k = k
        if l != -1:
            nodes[i].l = nodes[l]
        if r != -1:
            nodes[i].r = nodes[r]
    return nodes[0]


def solve(commands):
    if len(commands) == 0:
        is_correct = True
    else:
        root = build_tree(commands)
        is_correct = check_invariant_no_recursion(root)
    print('CORRECT' if is_correct else 'INCORRECT')


def main():
    reader = (s for s in sys.stdin)
    n = int(next(reader))
    commands = [list(map(int, next(reader).split())) for _ in range(n)]
    solve(commands)


if __name__ == "__main__":
    main()

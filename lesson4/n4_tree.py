import sys
from __future__ import annotations


class Node:
    L: str = 'l'
    R: str = 'r'

    def __init__(self, k, l=None, r=None, p=None):
        self.k: int = k
        self.p: Node = p
        self.children = {Node.L: l, Node.R: r}
        # todo: calc heights if l or r is not None
        self.weights = {Node.L: 0, Node.R: 0}

    @property
    def lh(self) -> int:
        return self.weights[Node.L]

    @property
    def lh(self, v):
        self.weights[Node.L] = v

    @property
    def rh(self) -> int:
        return self.weights[Node.R]

    @property
    def rh(self, v):
        self.weights[Node.R] = v

    @property
    def l(self) -> Node:
        return self.children[Node.L]

    @property
    def l(self, node: Node):
        self.set_child(Node.L, node)

    @property
    def r(self) -> Node:
        return self.children[Node.R]

    @property
    def r(self, node: Node):
        self.set_child(Node.R, node)

    def set_child(self, child_type: str, node: Node):
        self.children[child_type] = node
        if node is not None:
            self.weights[child_type] = max(node.lh, node.rh) + 1
            # reset parent
            if node.p is not None:
                child_type = node.p.get_child_type(node)
                node.p.set_child(child_type, None)
            node.p = self
        else:
            self.weights[child_type] = 0

    def get_child_type(self, node: Node) -> str:
        return Node.L if node.k < self.k else Node.R


def small_rotation(is_left: bool, alpha: Node, beta: Node, b: Node):
    if is_left:
        alpha.l = b
        beta.r = alpha
    else:
        alpha.r = b
        beta.l = alpha
    beta.p = None
    return beta


def big_rotation(is_left: bool, alpha: Node, beta: Node, gamma: Node, b: Node, c):
    if is_left:
        alpha.r = b
        beta.l = c
        gamma.l = alpha
        gamma.r = beta
    else:
        alpha.r = b
        beta.l = c
        gamma.l = alpha
        gamma.r = beta
    gamma.p = None
    return gamma


def repair_invariant(node: Node):
    if abs(node.lh - node.rh) <= 1:
        return node

    alpha: Node = node
    beta: Node = None
    gamma: Node = None
    is_left = alpha.lh > alpha.rh
    is_small = False
    if is_left:
        beta = alpha.l
        if beta.rh <= beta.lh:
            b = beta.r
            is_small = True
        else:
            gamma = beta.r
            b = gamma.r
            c = gamma.l
    else:
        beta = alpha.r
        if beta.lh <= beta.rh:
            b = beta.l
            is_small = True
        else:
            gamma = beta.l
            b = gamma.l
            c = gamma.r

    if is_small:
        return small_rotation(is_left, alpha, beta, b)
    else:
        return big_rotation(is_left, alpha, beta, gamma, b, c)


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
            else:
                self._add(node.l, new_node)
        else:
            if node.r is None:
                node.r = new_node
                new_node.p = node
            else:
                self._add(node.r, new_node)
        return new_node

    def remove(self, k):
        pass


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
    root = build_tree(commands)
    print(root.lh, root.rh)

def main():
    reader = (s for s in sys.stdin)
    n = int(next(reader))
    commands = [list(map(int, next(reader).split())) for _ in range(n)]
    solve(commands)


if __name__ == "__main__":
    main()

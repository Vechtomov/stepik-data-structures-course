import sys
from __future__ import annotations
from typing import Tuple


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
    def lh(self, value):
        self.weights[Node.L] = value

    @property
    def rh(self) -> int:
        return self.weights[Node.R]

    @property
    def rh(self, value):
        self.weights[Node.R] = value

    @property
    def l(self) -> Node:
        return self[Node.L]

    @property
    def l(self, node: Node):
        self[Node.L] = node

    @property
    def r(self) -> Node:
        return self[Node.R]

    @property
    def r(self, node: Node):
        self[Node.R] = node

    def get_child_type(self, node: Node) -> str:
        return Node.L if node.k < self.k else Node.R

    def __getitem__(self, child_type: str) -> Node:
        return self.children[child_type]

    def __setitem__(self, child_type: str, node: Node):
        self.children[child_type] = node
        if node is not None:
            self.weights[child_type] = max(node.lh, node.rh) + 1
            # reset parent
            if node.p is not None:
                child_type = node.p.get_child_type(node)
                node.p[child_type] = None
            node.p = self
        else:
            self.weights[child_type] = 0

    def __delitem__(self, child_type):
        self[child_type] = None


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


def repair_invariant(node: Node) -> Tuple[Node, bool]:
    if node is None:
        return node, False
    if abs(node.lh - node.rh) <= 1:
        return node, False

    alpha: Node = node
    beta: Node = None
    gamma: Node = None
    b: Node = None
    c: Node = None
    is_left = alpha.lh > alpha.rh
    is_small_rotation = False
    if is_left:
        beta = alpha.l
        if beta.rh <= beta.lh:
            b = beta.r
            is_small_rotation = True
        else:
            gamma = beta.r
            b = gamma.r
            c = gamma.l
    else:
        beta = alpha.r
        if beta.lh <= beta.rh:
            b = beta.l
            is_small_rotation = True
        else:
            gamma = beta.l
            b = gamma.l
            c = gamma.r

    if is_small_rotation:
        root = small_rotation(is_left, alpha, beta, b)
    else:
        root = big_rotation(is_left, alpha, beta, gamma, b, c)

    return root, True


class Tree:
    def __init__(self) -> None:
        self.root = None

    def add(self, k: int):
        if self.root is None:
            self.root = Node(k)
        else:
            self._add(self.root, Node(k))

    def _add(self, node: Node, new_node: Node):
        child_type = node.get_child_type(new_node)
        if node[child_type] is None:
            node[child_type] = new_node
            self._repair(new_node)
        else:
            self._add(node.l, new_node)
        return new_node

    def remove(self, k: int):
        if self.root is None:
            return
        self._remove(self.root, k)

    def _remove(self, node: Node, k: int):
        if node.k == k:
            self._remove_node(node)
        else:
            child_type = node.get_child_type(Node(k))
            child_node = node[child_type]
            if child_node is not None:
                self._remove(child_node, k)

    def _remove_node(self, node: Node):
        existed_child_types = [
            t for t, n in node.children.items() if n is not None]
        is_root = node.p is None
        node_type = None if is_root else node.p.get_child_type(node)
        if len(existed_child_types) == 0:
            self._remove_node_no_children(node, is_root, node_type)
        elif len(existed_child_types) == 1:
            self._remove_node_one_child(
                node, existed_child_types[0], is_root, node_type)
        else:
            self._remove_node_two_children(node, is_root, node_type)

    def _remove_node_no_children(self, node: Node, is_root: bool, node_type: str):
        if is_root:
            self.root = None
        else:
            del node.p[node_type]
            self._repair(node.p)

    def _remove_node_one_child(self, node: Node, child_type: str, is_root: bool, node_type: str):
        child = node[child_type]
        if is_root:
            self.root = child
        else:
            node.p[node_type] = child
        self._repair(child)

    def _remove_node_two_children(self, node: Node, is_root: bool, node_type: str):
        max_r_child: Node = node.l
        while max_r_child.r is not None:
            max_r_child = max_r_child.r

        if max_r_child == node.l:
            max_r_child.r = node.r
            repair_node = max_r_child
        else:
            repair_node = max_r_child.p
            max_r_child.p.r = None
            max_r_child.l = node.l
            max_r_child.r = node.r
        if is_root:
            self.root = max_r_child
        else:
            node.p[node_type] = max_r_child
        self._repair(repair_node)

    def _repair(self, node: Node):
        node, changed = repair_invariant(node)
        if changed:
            self._repair(node.p)


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

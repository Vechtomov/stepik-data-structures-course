from __future__ import annotations
from ctypes import Union
import sys
from typing import Tuple


class Node:
    L: str = 'l'
    R: str = 'r'

    def __init__(self, k: int):
        self.k: int = k
        self._p: Node = None
        self.children = {Node.L: None, Node.R: None}
        self.heights = {Node.L: 0, Node.R: 0}
        self.sums = {Node.L: 0, Node.R: 0}

    @property
    def lh(self) -> int:
        return self.heights[Node.L]

    @property
    def rh(self) -> int:
        return self.heights[Node.R]

    @property
    def ls(self) -> int:
        return self.sums[Node.L]

    @property
    def rs(self) -> int:
        return self.sums[Node.R]

    @property
    def l(self) -> Node:
        return self[Node.L]

    @l.setter
    def l(self, node: Node):
        self[Node.L] = node

    @property
    def r(self) -> Node:
        return self[Node.R]

    @r.setter
    def r(self, node: Node):
        self[Node.R] = node

    @property
    def p(self) -> Node:
        return self._p

    @p.setter
    def p(self, parent: Node):
        current_parent = self.p
        if current_parent is not None:
            current_parent.remove_child(self)
        if parent is not None:
            parent.set_child(self)

    def get_child_type(self, node: Node) -> str:
        assert node is not None
        return Node.L if node.k < self.k else Node.R

    def set_child(self, child: Node):
        assert child is not None
        child_type = self.get_child_type(child)
        self[child_type] = child

    def remove_child(self, child: Node) -> bool:
        if child is None:
            return
        child_type = self.get_child_type(child)
        if self[child_type] == child:
            del self[child_type]
            return True
        else:
            return False

    def __getitem__(self, child_type: str) -> Node:
        return self.children[child_type]

    def __setitem__(self, child_type: str, child: Node):
        assert child is None or child.p is None
        current_child = self[child_type]
        if current_child is not None:
            current_child._p = None
        self.children[child_type] = child
        self.recalc_stats(child_type)
        if child is not None:
            child._p = self

    def __delitem__(self, child_type):
        self[child_type] = None

    def __str__(self) -> str:
        p_str = self.p.k if self.p else 'null'
        return f"{self.k}({p_str}) {{lh: {self.lh}, rh: {self.rh}, ls: {self.ls}, rs: {self.rs}}}"

    def __repr__(self) -> str:
        p_str = self.p.k if self.p else 'null'
        return f"{self.k}({p_str})"

    def recalc_stats(self, child_type=None):
        child_types = [Node.L, Node.R] if child_type is None else [child_type]
        for t in child_types:
            child = self[t]
            self.heights[t] = 0 if child is None else \
                max(child.lh, child.rh) + 1
            self.sums[t] = 0 if child is None else \
                child.ls + child.rs + child.k


def small_rotation(is_left: bool, alpha: Node, beta: Node):
    alpha_p = alpha.p
    alpha.p = None
    alpha.remove_child(beta)
    b = beta.r if is_left else beta.l
    beta.remove_child(b)
    if is_left:
        alpha.l = b
        beta.r = alpha
    else:
        alpha.r = b
        beta.l = alpha
    beta.p = alpha_p
    return beta


def big_rotation(is_left: bool, alpha: Node, beta: Node):
    alpha_p = alpha.p
    gamma = beta.r if is_left else beta.l
    b = gamma.r if is_left else gamma.l
    c = gamma.l if is_left else gamma.r
    alpha.p = None
    beta.p = None
    gamma.p = None
    gamma.remove_child(b)
    gamma.remove_child(c)
    if is_left:
        alpha.l = b
        beta.r = c
        gamma.r = alpha
        gamma.l = beta
    else:
        alpha.r = b
        beta.l = c
        gamma.l = alpha
        gamma.r = beta
    gamma.p = alpha_p
    return gamma


def repair_invariant(node: Node) -> Tuple[Node, bool]:
    if node is None:
        return node, False
    node.recalc_stats()
    if abs(node.lh - node.rh) <= 1:
        return node, False

    alpha: Node = node
    beta: Node = None
    is_left = alpha.lh > alpha.rh
    beta = alpha.l if is_left else alpha.r
    if is_left:
        is_small_rotation = beta.rh <= beta.lh
    else:
        is_small_rotation = beta.lh <= beta.rh

    if is_small_rotation:
        root = small_rotation(is_left, alpha, beta)
    else:
        root = big_rotation(is_left, alpha, beta)

    return root, True


def merge_trees(t1: Tree, t2: Tree) -> Tree:
    assert t1 is not None and t2 is not None
    if abs(t1.h - t2.h) <= 1:
        if t1.h > t2.h:
            t = t1
            root = t.max()
        else:
            t = t2
            root = t.min()
        t.remove(root.k)
        root.l = t1.root
        root.r = t2.root
        t = Tree(root)
        return t
    elif t1.h > t2.h:
        r = t1.root.r
        t1.root.r = None
        t = merge_trees(Tree(r), t2)
        t1.add(t.root)
        return t1
    else:
        l = t2.root.l
        t2.root.l = None
        t = merge_trees(t1, Tree(l))
        t2.add(t.root)
        return t2


def split_tree(t: Tree, k: int) -> Tuple[Tree, Tree]:
    if t.root is None:
        return None, None
    root = t.root
    l_node, r_node = root.l, root.r
    root.l = None
    root.r = None
    l_tree, r_tree = Tree(l_node), Tree(r_node)
    if k < root.k:
        r_tree.add(root)
        l_tree, r = split_tree(l_tree, k)
        if r is not None:
            r_tree = merge_trees(r, r_tree)
    else:
        l_tree.add(root)
        l, r_tree = split_tree(r_tree, k)
        if l is not None:
            l_tree = merge_trees(l_tree, l)
    return l_tree, r_tree


class Tree:
    def __init__(self, root: Node = None) -> None:
        self.root = root

    @property
    def h(self) -> int:
        if self.root is None:
            return 0
        return max(self.root.lh, self.root.rh) + 1

    def add(self, v: Union[int, Node]):
        node = v if isinstance(v, Node) else Node(v)
        if self.root is None:
            self.root = node
        else:
            self._add(self.root, node)

    def _add(self, node: Node, new_node: Node):
        child_type = node.get_child_type(new_node)
        child = node[child_type]
        if child is None:
            node[child_type] = new_node
            self._repair(new_node)
        else:
            self._add(child, new_node)

    def find(self, k: int) -> Node:
        return self._find(self.root, k)

    def _find(self, node: Node, k: int) -> Node:
        if node is None:
            return False
        if node.k == k:
            return True
        return self._find(node.l if k < node.k else node.r, k)

    def max(self) -> Node:
        assert self.root is not None
        return self._find_max(self.root)

    def min(self) -> Node:
        assert self.root is not None
        return self._find_min(self.root)

    def _find_max(self, node: Node):
        assert node is not None
        curr = node
        while curr.r is not None:
            curr = curr.r
        return curr
        
    def _find_min(self, node: Node):
        assert node is not None
        curr = node
        while curr.l is not None:
            curr = curr.l
        return curr

    def remove(self, v: Union[int, Node]):
        if self.root is None or v is None:
            return
        k = v.k if isinstance(v, Node) else v
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
            parent = node.p
            node.p = None
            self._repair(parent)

    def _remove_node_one_child(self, node: Node, child_type: str, is_root: bool, node_type: str):
        child = node[child_type]
        child.p = None
        if is_root:
            self.root = child
        else:
            node.p[node_type] = child
        self._repair(child)

    def _remove_node_two_children(self, node: Node, is_root: bool, node_type: str):
        max_left_child: Node = self._find_max(node.l)
        l = node.l
        r = node.r
        node.remove_child(l)
        node.remove_child(r)

        if max_left_child == l:
            repair_node = max_left_child
            max_left_child.r = r
        else:
            repair_node = max_left_child.p
            max_left_child.p = None
            max_left_child.l = l
            max_left_child.r = r
        if is_root:
            self.root = max_left_child
        else:
            node.p[node_type] = max_left_child
        self._repair(repair_node)

    def _repair(self, node: Node):
        node, _ = repair_invariant(node)
        if node.p is not None:
            self._repair(node.p)
        else:
            self.root = node


def build_tree(commands) -> Tree:
    pass


def solve(commands):
    tree = build_tree(commands)
    print(tree.root.lh, tree.root.rh)


def main():
    reader = (s for s in sys.stdin)
    n = int(next(reader))
    commands = [list(map(int, next(reader).split())) for _ in range(n)]
    solve(commands)


if __name__ == "__main__":
    main()

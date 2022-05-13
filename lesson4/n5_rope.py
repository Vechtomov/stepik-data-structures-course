from __future__ import annotations
import sys
from typing import Tuple


class Node:
    L: str = 0
    R: str = 1

    def __init__(self, s: str):
        self.s: str = s
        self.p: Node = None
        self.lh = 0
        self.rh = 0
        self.counts = [0, 0]
        self.height_changed = False
        self.children = [None, None]

    @property
    def l(self) -> Node:
        return self.children[Node.L]

    @l.setter
    def l(self, node: Node):
        self[Node.L] = node

    @property
    def r(self) -> Node:
        return self.children[Node.R]

    @r.setter
    def r(self, node: Node):
        self[Node.R] = node

    def detach(self):
        if self.p is not None:
            self.p.remove_child(self)

    def get_child_type(self, node: Node) -> str:
        assert node is not None
        if node == self.l:
            return Node.L
        elif node == self.r:
            return Node.R
        else:
            return None

    def remove_child(self, child: Node) -> bool:
        if child is None:
            return
        child_type = self.get_child_type(child)
        if child_type is not None:
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
            current_child.p = None
        self.children[child_type] = child
        self._recalc_child_stats(child_type)
        if child is not None:
            child.p = self

    def __delitem__(self, child_type):
        self[child_type] = None

    def __repr__(self) -> str:
        p_str = self.p.s if self.p else 'null'
        return f"{self.s}({p_str})"

    def recalc_height(self):
        self._recalc_height(Node.L)
        self._recalc_height(Node.R)
        self.height_changed = False

    def recalc_count(self):
        self._recalc_count(Node.L)
        self._recalc_count(Node.R)

    def _recalc_child_stats(self, child_type: str):
        self._recalc_height(child_type)
        self._recalc_count(child_type)

    def _recalc_count(self, child_type: str):
        child = self[child_type]
        self.counts[child_type] = 0 if child is None else child.counts[Node.L] + \
            child.counts[Node.R] + 1

    def _recalc_height(self, child_type: str):
        child = self[child_type]
        new_height = 0 if child is None else \
            (child.lh if child.lh > child.rh else child.rh) + 1
        if child_type == Node.L:
            last_height = self.lh
            self.lh = new_height
        else:
            last_height = self.rh
            self.rh = new_height
        if last_height != new_height:
            if self.p is not None:
                self.p.height_changed = True


def small_rotation(is_left: bool, alpha: Node, beta: Node):
    alpha_p = alpha.p
    if alpha_p is not None:
        alpha_child_type = alpha_p.get_child_type(alpha)
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
    if alpha_p is not None:
        alpha_p.children[alpha_child_type] = beta
        beta.p = alpha_p
        alpha_p.height_changed = True
    return beta


def big_rotation(is_left: bool, alpha: Node, beta: Node):
    alpha_p = alpha.p
    if alpha_p is not None:
        alpha_child_type = alpha_p.get_child_type(alpha)
        alpha.p = None
    gamma = beta.r if is_left else beta.l
    b = gamma.r if is_left else gamma.l
    c = gamma.l if is_left else gamma.r
    beta.detach()
    gamma.detach()
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
    if alpha_p is not None:
        alpha_p.children[alpha_child_type] = gamma
        gamma.p = alpha_p
        alpha_p.height_changed = True
    return gamma


def repair_invariant(node: Node) -> Tuple[Node, bool]:
    if node is None:
        return node, False
    if node.height_changed:
        node.recalc_height()
    node.recalc_count()
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
    if t1.root is None:
        return t2
    if t2.root is None:
        return t1
    if abs(t1.h - t2.h) <= 1:
        if t1.h > t2.h:
            t = t1
            root = t.max()
        else:
            t = t2
            root = t.min()
        t.remove(root)
        root.l = t1.root
        root.r = t2.root
        t = Tree(root)
        return t
    elif t1.h > t2.h:
        r = t1.root.r
        t1.root.r = None
        t = merge_trees(Tree(r), t2)
        t1.add_max(t.root)
        return t1
    else:
        l = t2.root.l
        t2.root.l = None
        t = merge_trees(t1, Tree(l))
        t2.add_min(t.root)
        return t2


def split_tree(t: Tree, i: int) -> Tuple[Tree, Tree]:
    if t.root is None:
        return Tree(), Tree()
    root = t.root
    l_node, r_node = root.l, root.r
    left_count = root.counts[Node.L] + 1
    root.l = None
    root.r = None
    l_tree, r_tree = Tree(l_node), Tree(r_node)
    if i == left_count:
        r_tree.add_min(root)
        return l_tree, r_tree
    elif i < left_count:
        r_tree.add_min(root)
        l_tree, r = split_tree(l_tree, i)
        r_tree = merge_trees(r, r_tree)
    else:
        l_tree.add_max(root)
        l, r_tree = split_tree(r_tree, i - left_count)
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

    @property
    def count(self) -> int:
        if self.root is None:
            return 0
        return self.root.counts[Node.L] + self.root.counts[Node.R] + 1

    def add_max(self, node: Node):
        assert node is not None
        if self.root is None:
            self.root = node
        else:
            max_node = self._find_max(self.root)
            max_node.r = node
            self._repair(node)

    def add_min(self, node: Node):
        assert node is not None
        if self.root is None:
            self.root = node
        else:
            min_node = self._find_min(self.root)
            min_node.l = node
            self._repair(node)

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

    def remove(self, node: Node):
        self._remove_node(node)

    def _remove_node(self, node: Node):
        existed_child_types = [
            t for t in [Node.L, Node.R] if node[t] is not None]
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
            node.detach()
            self._repair(parent)

    def _remove_node_one_child(self, node: Node, child_type: str, is_root: bool, node_type: str):
        child = node[child_type]
        child.detach()
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
            ml = max_left_child.l
            max_left_child.remove_child(ml)
            repair_node.r = ml
            max_left_child.detach()
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


def build_tree(s: str):
    t = Tree()
    for c in s:
        t.add_max(Node(c))
    return t


def permute(t: Tree, beg: int, end: int, pos: int) -> Tree:
    left_t, right_t = split_tree(t, beg + 1)
    center_t, right_t = split_tree(right_t, end - beg + 2)
    t = merge_trees(left_t, right_t)
    left_t, right_t = split_tree(t, pos + 1)
    t = merge_trees(left_t, center_t)
    t = merge_trees(t, right_t)
    return t


def in_order(node: Node):
    if node is None:
        return
    for n in in_order(node.l):
        yield n
    yield node
    for n in in_order(node.r):
        yield n


def get_string(t: Tree) -> str:
    return ''.join([n.s for n in in_order(t.root)])


def solve(s, commands):
    t = build_tree(s)
    for beg, end, pos in commands:
        t = permute(t, beg, end, pos)
    return get_string(t)


def main():
    reader = (s for s in sys.stdin)
    s = next(reader).strip()
    n = int(next(reader))
    commands = [list(map(int, next(reader).split())) for _ in range(n)]
    r = solve(s, commands)
    print(r)


if __name__ == "__main__":
    main()

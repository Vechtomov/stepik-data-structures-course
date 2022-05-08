from __future__ import annotations
import sys
from typing import Tuple, Union


class Node:
    L: str = 'l'
    R: str = 'r'

    def __init__(self, k: int):
        self.k: int = k
        self._p: Node = None
        self._l = None
        self._r = None
        self.lh = 0
        self.rh = 0
        self.ls = 0
        self.rs = 0
        self.height_changed = False

    @property
    def l(self) -> Node:
        return self._l

    @l.setter
    def l(self, node: Node):
        self[Node.L] = node

    @property
    def r(self) -> Node:
        return self._r

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
        return self._l if child_type == Node.L else self._r

    def __setitem__(self, child_type: str, child: Node):
        assert child is None or child.p is None
        current_child = self[child_type]
        if current_child is not None:
            current_child._p = None
        if child_type == Node.L:
            self._l = child
        else:
            self._r = child
        self._recalc_child_stats(child_type)
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

    def recalc_height(self):
        for t in [Node.L, Node.R]:
            self._recalc_height(t)
        self.height_changed = False

    def recalc_sum(self):
        for t in [Node.L, Node.R]:
            self._recalc_sum(t)

    def _recalc_child_stats(self, child_type: str):
        self._recalc_height(child_type)
        self._recalc_sum(child_type)

    def _recalc_sum(self, child_type: str):
        child = self[child_type]
        new_sum = 0 if child is None else \
            child.ls + child.rs + child.k
        if child_type == Node.L:
            self.ls = new_sum
        else:
            self.rs = new_sum

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
    if node.height_changed:
        node.recalc_height()
    node.recalc_sum()
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
        return Tree(), Tree()
    root = t.root
    l_node, r_node = root.l, root.r
    root.l = None
    root.r = None
    l_tree, r_tree = Tree(l_node), Tree(r_node)
    if k < root.k:
        r_tree.add(root)
        l_tree, r = split_tree(l_tree, k)
        r_tree = merge_trees(r, r_tree)
    else:
        l_tree.add(root)
        l, r_tree = split_tree(r_tree, k)
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
    def sum(self) -> int:
        if self.root is None:
            return 0
        return self.root.ls + self.root.rs + self.root.k

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

    def find(self, k: int) -> bool:
        return self._find(self.root, k)

    def _find(self, node: Node, k: int) -> bool:
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
            t for t in [Node.L, Node.r] if node[t] is not None]
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
            ml = max_left_child.l
            max_left_child.remove_child(ml)
            repair_node.r = ml
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

def sum_segment(t: Tree, l: int, r: int) -> int:
    left_t, right_t = split_tree(t, l-1)
    center_t, right_t = split_tree(right_t, r)
    res = center_t.sum
    left_t = merge_trees(left_t, center_t)
    t = merge_trees(left_t, right_t)
    return res, t

def solve(commands):
    t = Tree()
    s = 0
    p = 1_000_000_001

    def f(x):
        return (x % p + s) % p

    for comm in commands:
        c, args = comm[0], list(map(int, comm[1:]))
        if c == 's':
            l, r = map(f, args)
            res, t = sum_segment(t, l, r)
            s = res % p
            yield str(res)
        else:
            i = f(args[0])
            if c == '+':
                if not t.find(i):
                    t.add(i)
            elif c == '-':
                t.remove(i)
            else:
                yield 'Found' if t.find(i) else 'Not found'


def main():
    reader = (s for s in sys.stdin)
    n = int(next(reader))
    commands = [next(reader).split() for _ in range(n)]
    for r in solve(commands):
        print(r)


if __name__ == "__main__":
    main()

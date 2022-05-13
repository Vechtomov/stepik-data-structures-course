from n5_rope import build_tree, Tree, Node, get_string, merge_trees, split_tree, permute, solve
import string
from typing import List, Tuple, Union, Callable
import random

NodeT = Tuple[int, Union[int, None]]
InOrderResult = List[NodeT]


def in_order(node: Node):
    if node is None:
        return
    for n in in_order(node.l):
        yield n
    yield node
    for n in in_order(node.r):
        yield n


def in_order_keys(node: Union[Node, Tree]):
    if isinstance(node, Tree):
        node = node.root
    result = []
    for n in in_order(node):
        result.append(int(n.s))
    return result


def are_equal(expected, actual):
    assert expected == actual, f"Expected: {expected}, Actual: {actual}"


def check_tree(t: Tree):
    def h(node: Node):
        return 0 if node is None else max(node.lh, node.rh) + 1

    def c(node: Node):
        return 0 if node is None else node.counts[Node.L] + node.counts[Node.R] + 1

    def check_node(node: Node):
        if node is None:
            return
        try:
            are_equal(h(node.l), node.lh)
            are_equal(h(node.r), node.rh)
            are_equal(c(node.l), node.counts[Node.L])
            are_equal(c(node.r), node.counts[Node.R])
            assert abs(node.lh - node.rh) <= 1, f"lh: {node.lh} rh: {node.rh}"
            check_node(node.l)
            check_node(node.r)
        except AssertionError:
            raise

    check_node(t.root)


def test_tree(t: Tree, result: InOrderResult):
    check_tree(t)
    transform: Callable[[Node], NodeT] = lambda n: (
        int(n.s), int(n.p.s) if n.p else None)
    actual = list(map(transform, in_order(t.root)))
    are_equal(result, actual)


def build_tree(nodes, to_right=True):
    t = Tree()
    for i in nodes:
        if to_right:
            t.add_max(Node(str(i)))
        else:
            t.add_min(Node(str(i)))
    return t


def test_tree_add():
    def test(nodes, result: InOrderResult):
        test_tree(build_tree(nodes), result)

    def test_left(nodes, result: InOrderResult):
        test_tree(build_tree(nodes, to_right=False), result)

    test([1], [(1, None)])
    test([1, 2], [(1, None), (2, 1)])
    test([1, 2, 3], [(1, 2), (2, None), (3, 2)])
    test_left([3, 2, 1], [(1, 2), (2, None), (3, 2)])

def test_tree_remove():
    def test(nodes: List[int], remove_node: int, result):
        t = build_tree(nodes)
        t.remove(remove_node)
        test_tree(t, result)

    test([0], 0, [])
    test([0, 1], 0, [(1, None)])
    test([0, 1, 2], 1, [(0, None), (2, 0)])

    nodes = list(range(5))
    test(nodes, 0, [(1, 3), (2, 1), (3, None), (4, 3)])
    test(nodes, 1, [(0, 3), (2, 0), (3, None), (4, 3)])
    test(nodes, 2, [(0, 1), (1, None), (3, 1), (4, 3)])
    test(nodes, 3, [(0, 1), (1, None), (2, 1), (4, 2)])
    test(nodes, 4, [(0, 1), (1, None), (2, 3), (3, 1)])


def test_tree_merge():
    def test(nodes1: Tree, nodes2: Tree, result: InOrderResult):
        t1 = build_tree(nodes1)
        t2 = build_tree(nodes2)
        t = merge_trees(t1, t2)
        test_tree(t, result)

    test([1], [2], [(1, 2), (2, None)])
    test([1], [2, 3], [(1, 2), (2, None), (3, 2)])
    test([1, 2], [3, 4], [(1, 3), (2, 1), (3, None), (4, 3)])
    test([1], [2,3,4,5,6], [(1, 2), (2, 3), (3, None), (4, 5), (5, 3), (6, 5)])


def test_tree_split():
    def test(nodes: Tree, k, r1: InOrderResult, r2: InOrderResult):
        t = build_tree(nodes)
        t1, t2 = split_tree(t, k)
        test_tree(t1, r1)
        test_tree(t2, r2)

    test([1], 0, [], [(1, None)])
    test([1], 1, [], [(1, None)])
    test([1], 2, [(1, None)], [])
    test([1, 2], 0, [], [(1, 2), (2, None)])
    test([1, 2], 1, [], [(1, 2), (2, None)])
    test([1, 2], 2, [(1, None)], [(2, None)])
    test([1, 2], 3, [(1, 2), (2, None)], [])
    test([1, 2, 3], 0, [], [(1, 2), (2, None), (3, 2)])


def test_solution():
    def test(s, commands, expected):
        actual = solve(s, [map(int, x.split()) for x in commands])
        are_equal(expected, actual)

    test('a', ['0 0 0'], 'a')
    test('ab', ['0 0 0'], 'ab')
    test('ab', ['0 0 1'], 'ba')
    test('ab', ['1 1 0'], 'ba')
    test('ab', ['0 1 0'], 'ab')
    test('hlelowrold', ['1 1 2', '6 6 7'], 'helloworld')

def test_permute_random(n = 100):
    def permute_baseline(s, beg, end, pos):
        substr = s[beg:end+1]
        s1 = s[:beg] + s[end+1:]
        return s1[:pos] + substr + s1[pos:]

    def test(s, beg, end, pos):
        t = build_tree(list(s))
        expected = permute_baseline(s, beg, end, pos)
        t = permute(t, beg, end, pos)
        are_equal(expected, get_string(t))

    s = string.ascii_uppercase
    l = len(s) - 1

    for _ in range(n):
        beg = random.randint(0, l)
        end = random.randint(beg, l)
        pos = random.randint(0, l - (end - beg))
        test(s, beg, end, pos)

def test_tree_random_add_remove(n=100):
    for i in range(n):
        nodes = list(range(100))
        random.shuffle(nodes)
        node_to_remove = nodes.copy()
        random.shuffle(node_to_remove)
        t = build_tree(nodes)
        check_tree(t)
        try:
            for k in node_to_remove:
                node_list = list(in_order(t.root))
                node_to_remove = random.choice(node_list)
                t.remove(node_to_remove)
                check_tree(t)
        except AssertionError as e:
            print(e)
            print(node_list)
            print(node_to_remove)
            raise
        assert t.root is None


def test_tree_random_split(n=100):
    for i in range(n):
        nodes = list(range(100))
        random.shuffle(nodes)
        keys = nodes.copy()
        random.shuffle(keys)
        try:
            for i in range(len(keys)):
                t = build_tree(nodes)
                t_keys = in_order_keys(t)
                t1, t2 = split_tree(t, i)
                check_tree(t1)
                check_tree(t2)
                t1_keys = in_order_keys(t1)
                t2_keys = in_order_keys(t2)
                # assert all(map(lambda x: x <= k, t1_keys)), f"{t1_keys} <= {k}"
                # assert all(map(lambda x: x > k, t2_keys)), f"{t2_keys} > {k}"
                are_equal(set(t_keys), set(t1_keys + t2_keys))
                are_equal(len(t_keys), len(t1_keys) + len(t2_keys))
        except AssertionError as e:
            print(e)
            print(nodes)
            raise


def test_tree_random_merge(n=100):
    for i in range(n):
        nodes = list(range(100))
        keys = nodes.copy()
        random.shuffle(keys)
        try:
            for k in keys:
                nodes1 = nodes[:k]
                random.shuffle(nodes1)
                nodes2 = nodes[k:]
                random.shuffle(nodes2)
                t1 = build_tree(nodes1)
                t2 = build_tree(nodes2)
                t1_keys = in_order_keys(t1)
                t2_keys = in_order_keys(t2)
                t = merge_trees(t1, t2)
                t_keys = in_order_keys(t)
                check_tree(t)
                are_equal(set(t1_keys + t2_keys), set(t_keys))
                are_equal(len(t1_keys) + len(t2_keys), len(t_keys))
        except AssertionError as e:
            print(e)
            print("Key:", k)
            print("Nodes1:", nodes1)
            print("Nodes2:", nodes2)
            raise


if __name__ == '__main__':
    test_tree_add()
    test_tree_random_add_remove(10)
    test_tree_merge()
    test_tree_split()
    test_tree_random_merge(10)
    test_tree_random_split(10)
    test_solution()
    test_permute_random(100)
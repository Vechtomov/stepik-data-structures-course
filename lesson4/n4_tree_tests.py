from n4_tree_no_annotations import Tree, Node, merge_trees, split_tree, solve, sum_segment, sum_segment_no_split
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
        result.append(n.k)
    return result


def are_equal(expected, actual):
    assert expected == actual, f"Expected: {expected}, Actual: {actual}"


def check_tree(t: Tree):
    def h(node: Node):
        return 0 if node is None else max(node.lh, node.rh) + 1

    def s(node: Node):
        return 0 if node is None else node.ls + node.rs + node.k

    def check_node(node: Node):
        if node is None:
            return
        try:
            are_equal(h(node.l), node.lh)
            are_equal(h(node.r), node.rh)
            are_equal(s(node.l), node.ls)
            are_equal(s(node.r), node.rs)
            assert abs(node.lh - node.rh) <= 1, f"lh: {node.lh} rh: {node.rh}"
            check_node(node.l)
            check_node(node.r)
        except AssertionError:
            raise

    check_node(t.root)


def show_tree(tree: Tree):
    for n in in_order(tree.root):
        h = max(n.lh, n.rh)
        print(''.join(['\t']*h) + repr(n))


def test_tree(t: Tree, result: InOrderResult):
    check_tree(t)
    transform: Callable[[Node], NodeT] = lambda n: (
        n.k, n.p.k if n.p else None)
    actual = list(map(transform, in_order(t.root)))
    are_equal(result, actual)


def build_tree(nodes):
    t = Tree()
    for i in nodes:
        t.add(i)
    return t


def build_n_tree(n):
    return build_tree(list(range(n)))


def test_tree_add():
    def test(nodes, result: InOrderResult):
        test_tree(build_tree(nodes), result)

    test([1], [(1, None)])
    test([1, 2], [(1, None), (2, 1)])
    test([2, 1], [(1, 2), (2, None)])
    # right small rotation
    test([1, 2, 3], [(1, 2), (2, None), (3, 2)])
    # left small rotation
    test([3, 2, 1], [(1, 2), (2, None), (3, 2)])
    # left big rotation
    test([4, 5, 1, 0, 2, 3], [(0, 1), (1, 2), (2, None), (3, 4), (4, 2), (5, 4)])
    # right big rotation
    test([1, 0, 4, 5, 3, 2], [(0, 1), (1, 3), (2, 1), (3, None), (4, 3), (5, 4)])


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
    test([1], [4, 5, 3, 2], [(1, 2), (2, 4), (3, 2), (4, None), (5, 4)])


def test_tree_split():
    def test(nodes: Tree, k, r1: InOrderResult, r2: InOrderResult):
        t = build_tree(nodes)
        t1, t2 = split_tree(t, k)
        test_tree(t1, r1)
        test_tree(t2, r2)

    test([1], 0, [], [(1, None)])
    test([1], 1, [(1, None)], [])
    test([1], 2, [(1, None)], [])
    test([1, 2], 0, [], [(1, 2), (2, None)])
    test([1, 2], 3, [(1, 2), (2, None)], [])
    test([1, 2], 1, [(1, None)], [(2, None)])
    test([1, 3, 4], 2, [(1, None)], [(3, 4), (4, None)])


def test_solution():
    def test(commands, expected):
        actual = list(solve(map(lambda x: x.split(), commands)))
        are_equal(expected, actual)

    test(['+ 1'], [])
    test(['- 1'], [])
    test(['? 1'], ['Not found'])
    test(['+ 1', '? 1'], ['Found'])
    test(['+ 1', '- 1', '? 1'], ['Not found'])
    test(['s 1 2'], ['0'])
    test(['+ 1', 's 1 2'], ['1'])
    test(['+ 1', '+ 2', 's 1 2'], ['3'])
    test(['+ 1', '+ 2', 's 1 2', '+ 1', 's 1 2'], ['3', '4'])
    test(['+ 1', '+ 2', 's 1 2', '+ 1', '? 1'], ['3', 'Found'])

    test(['+ 1_000_000_001', '? 0'], ['Found'])
    test(['+ 1_000_000_002', '? 1'], ['Found'])
    test(['+ 1_000_000_000', 's 0 1_000_000_000'], ['1000000000'])
    test(['+ 1_000_000_000', 's 0 1_000_000_000', '? 0'], ['1000000000', 'Found'])
    test(['+ 1', '+ 1_000_000_000', 's 0 1_000_000_000', '? 1'],
         ['1000000001', 'Found'])


def test_tree_random_add_remove(n=100):
    for i in range(n):
        nodes = list(range(100))
        random.shuffle(nodes)
        keys = nodes.copy()
        random.shuffle(keys)
        t = build_tree(nodes)
        check_tree(t)
        try:
            for k in keys:
                t.remove(k)
                check_tree(t)
        except AssertionError as e:
            print(e)
            print("Key:", k)
            print(nodes)
            print(keys)
            raise
        assert t.root is None


def test_tree_random_split(n=100):
    for i in range(n):
        nodes = list(range(100))
        random.shuffle(nodes)
        keys = nodes.copy()
        random.shuffle(keys)
        try:
            for k in keys:
                t = build_tree(nodes)
                t_keys = in_order_keys(t)
                t1, t2 = split_tree(t, k)
                check_tree(t1)
                check_tree(t2)
                t1_keys = in_order_keys(t1)
                t2_keys = in_order_keys(t2)
                assert all(map(lambda x: x <= k, t1_keys)), f"{t1_keys} <= {k}"
                assert all(map(lambda x: x > k, t2_keys)), f"{t2_keys} > {k}"
                are_equal(set(t_keys), set(t1_keys + t2_keys))
                are_equal(len(t_keys), len(t1_keys) + len(t2_keys))
        except AssertionError as e:
            print(e)
            print("Key:", k)
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


def test_tree_sum_segment():
    def test(nodes, l, r, expected):
        t = build_tree(nodes)
        t_keys = in_order_keys(t)
        s, tn = sum_segment_no_split(t, l, r)
        check_tree(tn)
        tn_keys = in_order_keys(tn)
        are_equal(expected, s)
        are_equal(t_keys, tn_keys)

    test([], 0, 0, 0)
    test([], 0, 1, 0)
    test([], 1, 1, 0)
    test([1], 0, 0, 0)
    test([1], 0, 1, 1)
    test([1], 1, 1, 1)
    test([1], 1, 2, 1)
    test([1], 2, 2, 0)
    test([1], 2, 3, 0)
    test([1, 2], 0, 0, 0)
    test([1, 2], 0, 1, 1)
    test([1, 2], 1, 1, 1)
    test([1, 2], 1, 2, 3)
    test([1, 2], 2, 2, 2)
    test([1, 2], 2, 3, 2)
    test([1, 2], 3, 3, 0)
    test([1, 2, 3, 4], 1, 2, 3)
    test([1, 2, 3, 4], 2, 3, 5)
    test([1, 2, 3, 4], 3, 4, 7)
    test([1, 2, 3, 4], 1, 3, 6)
    test([1, 2, 3, 4], 2, 4, 9)
    test([1, 2, 3, 4], 1, 4, 10)
    test([3, 2, 4, 1, 5], 2, 4, 9)

def test_tree_sum_segment_random(n=100):
    for i in range(n):
        arr = list(range(100))
        random.shuffle(arr)
        t = build_tree(arr)
        t_keys = in_order_keys(t)
        first = arr.copy()
        second = arr.copy()
        random.shuffle(first)
        random.shuffle(second)
        try:
            for f, s in zip(first, second):
                l, r = min(f, s), max(f, s)
                sum_actual, t = sum_segment_no_split(t, l, r)
                check_tree(t)
                t_keys_new = in_order_keys(t)
                are_equal(set(t_keys), set(t_keys_new))
                sum_expected = sum([x for x in t_keys if l <= x <= r])
                are_equal(sum_expected, sum_actual)
        except AssertionError as e:
            print(e)
            print("l:", l, "r:", r)
            print("Keys:", t_keys)
            raise


if __name__ == '__main__':
    test_tree_add()
    test_tree_remove()
    test_tree_random_add_remove(10)
    test_tree_merge()
    test_tree_split()
    test_tree_sum_segment()
    test_tree_random_merge(10)
    test_tree_random_split(10)
    test_tree_sum_segment_random(10)
    test_solution()

from n4_tree import sum_segment
from n4_tree_tests import build_tree
import random
import cProfile


def perf_sum_segment(n):
    arr = list(range(n))
    random.shuffle(arr)
    t = build_tree(arr)
    first = arr.copy()
    second = arr.copy()
    random.shuffle(arr)
    random.shuffle(first)
    random.shuffle(second)
    for f, s in zip(first, second):
        l, r = min(f, s), max(f, s)
        s, t = sum_segment(t, l, r)

if __name__ == "__main__":
    random.seed(0)
    cProfile.run('perf_sum_segment(1000)')


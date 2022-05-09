from n4_tree import sum_segment_no_split
from n4_tree_tests import build_tree
import random
import cProfile
import os
from datetime import datetime

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
        sm, t = sum_segment_no_split(t, l, r)

if __name__ == "__main__":
    random.seed(0)
    file = f'result_no_split_{datetime.now().strftime("%Y%m%d_%H%M%S")}.prof'
    cProfile.run('perf_sum_segment(10000)', file)
    os.system(f'snakeviz {file}')


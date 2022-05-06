import numpy as np

try:
    from functools import cache
except ImportError:
    from functools import lru_cache as cache

def solution_bottom_up(n, m):
    t = np.zeros((m, n), dtype=np.int32)
    for i in range(m):
        for j in range(n):
            left = t[i, j-1] if j - 1 > -1 else 0
            up = t[i-1, j] if i - 1 > -1 else 0
            t[i, j] = (left + up) or 1
    return t[m-1, n-1]

@cache
def solution_top_down(n, m):
    if n < 0 or m < 0:
        return 0
    if n == 1 and m == 1:
        return 1
    return solution_top_down(n-1, m) + solution_top_down(n, m-1)
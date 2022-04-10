import time

def timed_min(func, *args, n_iter = 10):
    acc = float("inf")
    for _ in range(n_iter):
        t0 = time.perf_counter()
        func(*args)
        t1 = time.perf_counter()
        acc = min(acc, t1 - t0)
    return acc

def timed_avg(func, *args, n_iter = 10):
    acc = 0
    for _ in range(n_iter):
        t0 = time.perf_counter()
        func(*args)
        t1 = time.perf_counter()
        acc += t1 - t0
    return acc / n_iter

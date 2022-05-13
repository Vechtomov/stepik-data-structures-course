from n5_rope import solve
import random
import cProfile
import os
from datetime import datetime


def perf_test(m):
    l = 10000
    commands = []
    for i in range(m):
        beg = random.randint(0, l)
        end = random.randint(beg, l)
        pos = random.randint(0, l - (end - beg))
        commands.append([beg, end, pos])

    solve('a' * (l + 1), commands)
 

if __name__ == "__main__":
    random.seed(0)
    file = f'rope_{datetime.now().strftime("%Y%m%d_%H%M%S")}.prof'
    cProfile.run('perf_test(1000)', file)
    os.system(f'snakeviz {file}')

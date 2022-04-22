from collections import deque
import sys


class Hash:
    def __init__(self, m, p=1_000_000_007, x=263) -> None:
        self.m = m
        self.p = p
        self.x = x
        self.powers = [1]

    def __call__(self, string) -> int:
        res = 0
        for i, ch in enumerate(string):
            res = (res + ord(ch)*self._x_pow(i)) % self.p
        return res % self.m

    def _x_pow(self, i):
        while i >= len(self.powers):
            self.powers.append((self.powers[-1] * self.x % self.p) % self.p)
        return self.powers[i]


def solve(m, commands):
    d = [deque() for _ in range(m)]
    h = Hash(m)
    for c, v in commands:
        if c == 'check':
            i = int(v)
            print(f'check {i}:', ' '.join(d[i]))
        else:
            i = h(v)
            if c == 'add' and v not in d[i]:
                print(f'add {v} in {i}')
                d[i].appendleft(v)
            elif c == 'del' and v in d[i]:
                print(f'del {v} from {i}')
                d[i].remove(v)
            elif c == 'find':
                print(f'find {v} in {i}:', v, 'yes' if v in d[i] else 'no')
        # print(d)


def main():
    reader = (s for s in sys.stdin)
    m = int(next(reader))
    n = int(next(reader))
    commands = [next(reader).split() for _ in range(n)]
    solve(m, commands)


if __name__ == "__main__":
    main()

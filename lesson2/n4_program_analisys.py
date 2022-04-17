import sys

class Vars:
    def __init__(self, n) -> None:
        self.weights = [1] * n
        self.links = [i for i in range(n)]

    def equal(self, i1, i2):
        l1 = self._get_link(i1)
        l2 = self._get_link(i2)
        if l1 == l2:
            return
        main, child = (l1, l2) if self.weights[l1] >= self.weights[l2] else (l2, l1)
        self.weights[main] += self.weights[child]
        self.links[child] = main

    def unequal(self, i1, i2):
        return self._get_link(i1) != self._get_link(i2)

    def _get_link(self, i):
        curr_i = i
        while self.links[curr_i] != curr_i:
            curr_i = self.links[curr_i]
        self.links[i] = curr_i
        return curr_i

def solve(n, equalities, inequalities):
    v = Vars(n)
    for x1, x2 in equalities:
        v.equal(x1 - 1, x2 - 1)
    for x1, x2 in inequalities:
        if not v.unequal(x1 - 1, x2 - 1):
            return False
    return True

def main():
    def read_list(s):
        return list(map(int, (s.split())))
    reader = (s for s in sys.stdin)
    n, e, d = read_list(next(reader))
    equalities = [read_list(next(reader)) for _ in range(e)]
    inequalities = [read_list(next(reader)) for _ in range(d)]
    res = solve(n, equalities, inequalities)
    print(int(res))

if __name__ == "__main__":
    main()
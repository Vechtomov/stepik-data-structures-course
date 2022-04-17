import sys

class Tables:
    def __init__(self, tables) -> None:
        self.tables = tables
        self.links = [i for i in range(len(tables))]
        self.max = max(tables)

    def join(self, i1, i2):
        l1 = self._get_link(i1)
        l2 = self._get_link(i2)
        if l1 == l2:
            return
        main, child = (l1, l2) if self.tables[l1] >= self.tables[l2] else (l2, l1)
        self.tables[main] += self.tables[child]
        self.tables[child] = 0
        self.links[child] = main
        if self.tables[main] > self.max:
            self.max = self.tables[main]

    def get_max(self):
        return self.max

    def _get_link(self, i):
        curr_i = i
        while self.links[curr_i] != curr_i:
            curr_i = self.links[curr_i]
        self.links[i] = curr_i
        return curr_i

def solve(tables, queries):
    t = Tables(tables)
    for t1, t2 in queries:
        t.join(t1 - 1, t2 - 1)
        print(t.get_max())

def main():
    def read_list(s):
        return list(map(int, (s.split())))
    reader = (s for s in sys.stdin)
    read_list(next(reader)) # skip numbers
    tables = read_list(next(reader))
    queries = [read_list(r) for r in reader]
    solve(tables, queries)

if __name__ == "__main__":
    main()
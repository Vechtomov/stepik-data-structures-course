from heapq import heappop, heappush
import sys

def main():
    def read_list(s):
        return list(map(int, (s.split())))
    reader = (s for s in sys.stdin)
    n, _ = read_list(next(reader))
    m = read_list(next(reader))
    h_p = [(0, p) for p in range(n)]
    print(len(m))
    for tn in m:
        t, p = heappop(h_p)
        print(p, " ", t)
        heappush(h_p, (t + tn, p))

if __name__ == "__main__":
    main()
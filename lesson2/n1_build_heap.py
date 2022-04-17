from __future__ import annotations
import sys

class MinHeap:
    def __init__(self, n) -> None:
        self.arr = [0] * n
        self.size = 0
        self.max_size = n

    def insert(self, value):
        assert self.size < self.max_size
        self.arr[self.size] = value
        self._sift_up(self.size)
        self.size += 1

    def extract_min(self):
        assert self.size > 0
        result = self.arr[0]
        self.arr[0] = self.arr[self.size - 1]
        self.size -= 1
        return result

    def get_min(self):
        assert self.size > 0
        return self.arr[0]

    def get_size(self):
        return self.size

    @staticmethod
    def _parent_ind(i):
        return (i - 1) // 2

    @staticmethod
    def _left_child_ind(i):
        return 2 * i + 1

    @staticmethod
    def _right_child_ind(i):
        return 2 * i + 2

    def _swap(self, i1, i2):
        self.arr[i1], self.arr[i2] = self.arr[i2], self.arr[i1]

    def _sift_up(self, i):
        while i > 0 and self.arr[i] < self.arr[self._parent_ind(i)]:
            self._swap(i, self._parent_ind(i))
            i = self._parent_ind(i)

    def _sift_down(self, i):
        while self._left_child_ind(i) < self.size:
            min_i = i
            left_i = self._left_child_ind(i)
            if self.arr[i] > self.arr[left_i]:
                min_i = left_i

            right_i = self._right_child_ind(i)
            if right_i < self.size and self.arr[min_i] > self.arr[right_i]:
                min_i = right_i

            if i == min_i:
                return

            self._swap(i, min_i)
            i = min_i

    def check(self):
        i = 0
        while i < self.size:
            if self._left_child_ind(i) < self.size:
                assert self.arr[i] < self.arr[self._left_child_ind(i)]
            if self._right_child_ind(i) < self.size:
                assert self.arr[i] < self.arr[self._right_child_ind(i)]
            i += 1


class MinHeapSwapLogging(MinHeap):
    def __init__(self, n) -> None:
        super().__init__(n)
        self.swaps = []

    def _swap(self, i1, i2):
        self.swaps.append((i1, i2))
        super()._swap(i1, i2)

    @staticmethod
    def build(arr) -> MinHeapSwapLogging:
        h = MinHeapSwapLogging(len(arr))
        h.arr = arr
        h.size = len(arr)
        for i in range(len(arr)//2, -1, -1):
            h._sift_down(i)
        return h

def main():
    def read_list(s):
        return list(map(int, (s.split())))
    reader = (s for s in sys.stdin)
    next(reader)
    h = MinHeapSwapLogging.build(read_list(next(reader)))
    print(len(h.swaps))
    for i1, i2 in h.swaps:
        print(i1, " ", i2)

if __name__ == '__main__':
    main()

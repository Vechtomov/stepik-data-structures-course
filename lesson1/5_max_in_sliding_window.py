import sys

class MaxWindow:
    def __init__(self):
        self.arr = []
        self.start_ind = 0

    def insert(self, value):
        while len(self.arr) - self.start_ind > 0:
            curr = self.arr.pop()
            if(curr >= value):
                self.arr.append(curr)
                break
        self.arr.append(value)

    def max(self):
        return self.arr[self.start_ind]

    def remove(self, value):
        if value == self.arr[self.start_ind]:
            self.start_ind += 1

def task(arr, size):
    window = MaxWindow(len(arr))
    result = []
    for i, item in enumerate(arr, start=1):
        window.insert(item)
        if i >= size:
            # print(window.arr, window.start_ind)
            result.append(window.max())
            window.remove(arr[i - size])
    return result

def main():
    def read_arr(s):
        return list(map(int, (s.split())))
    reader = (s for s in sys.stdin)
    next(reader)
    arr = read_arr(next(reader))
    result = task(arr, int(next(reader)))
    print(len(result))

def test():
    from utils import are_equal
    method = task
    def arr(s):
        return list(map(int, s.split()))

    def tests():
        are_equal(method([1], 1), [1])
        are_equal(method([1, 2, 3], 1), [1, 2, 3])
        are_equal(method([1, 2, 3], 2), [2, 3])
        are_equal(method([1, 2, 3, 4], 2), [2, 3, 4])
        are_equal(method([4, 3, 2, 1], 2), [4, 3, 2])
        are_equal(method([1, 2, 3], 3), [3])
        are_equal(method([3, 2, 1], 3), [3])
        are_equal(method([1, 3, 2], 3), [3])
        are_equal(method([1, 2, 3, 4], 3), [3, 4])
        are_equal(method([1, 2, 3, 3, 2, 1], 2), [2, 3, 3, 3, 2])
        are_equal(method([1, 2, 3, 3, 2, 1, 1], 2), [2, 3, 3, 3, 2, 1])

    def example_tests():
        are_equal(method(arr('2 7 3 1 5 2 6 2'), 4), arr('7 7 5 6 6'))

    tests()
    example_tests()

    print('all tests succeeded')

def performance():
    from utils import timed_min
    data = generate_test_data()
    generate_test_file(data)
    print(timed_min(task, *data, n_iter=2))

def generate_test_data():
    import random
    n = 10**5
    return [\
        # random.randint(-10**4, 10**4) \
        n - i \
        for i in range(n)], 50000

def generate_test_file(data):
    from utils import generate_test_file as generate
    generate('max_in_sliding_window_test.txt', [f'{len(data[0])}\n'] + [' '.join(map(str, data[0])) + '\n'] + [f'{data[1]}\n'])

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else None
    if(mode == 'performance'): performance()
    elif(mode == 'test'): test()
    else:
        from utils import timed_min
        print(timed_min(main, n_iter=1))
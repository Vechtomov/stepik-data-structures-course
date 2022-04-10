import sys, queue

def build_tree(a):
    res = [None] * len(a)
    root = -1
    for i, parent in enumerate(a):
        if parent == -1: root = i
        elif res[parent]: res[parent].append(i)
        else: res[parent] = [i]
    return res, root

def get_height(tree, root):
    q = queue.Queue(len(tree))
    max_height = 1
    q.put((root, max_height))
    while not q.empty():
        i, h = q.get()
        if h > max_height: 
            max_height = h
        if tree[i]:
            for el in tree[i]: q.put((el, h + 1))
    return max_height

def task(arr):
    tree, root = build_tree(arr)
    return get_height(tree, root)

def main():
    def read_arr(s):
        return list(map(int, (s.split())))
    reader = (s for s in sys.stdin)
    next(reader)
    result = task(read_arr(next(reader)))
    print(result)

def test():
    from utils import are_equal
    method = task

    def simple_tests():
        are_equal(method([-1]), 1)
        are_equal(method([-1, 0]), 2)
        are_equal(method([1, -1]), 2)
        are_equal(method([-1, 0, 0]), 2)
        are_equal(method([1, -1, 1]), 2)
        are_equal(method([2, 2, -1]), 2)
        are_equal(method([-1, 0, 1]), 3)
        are_equal(method([-1, 0, 1, 2]), 4)
        are_equal(method([-1, 0, 0, 0]), 2)

    def examples():
        are_equal(method([4, -1, 4, 1, 1]), 3)
        are_equal(method([-1, 0, 4, 0, 3]), 4)
        are_equal(method([9, 7, 5, 5, 2, 9, 9, 9, 2, -1]), 4)
    
    simple_tests()
    examples()

    print('all tests succeeded')

def performance():
    from utils import timed_min
    data = generate_test_data()
    generate_test_file(data)
    print(timed_min(task, data, n_iter=2))
    
def generate_test_data():
    n = 10**5
    return [i for i in range(-1, n)]

def generate_test_file(data):
    from utils import generate_test_file as generate
    s = ' '.join(map(str, data))
    generate('tree_height_test.txt', [f'{len(data)}\n'] + [f'{s}\n'])

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else None
    if(mode == 'performance'): performance()
    elif(mode == 'test'): test()
    else: 
        from utils import timed_min
        print(timed_min(main, n_iter=1))
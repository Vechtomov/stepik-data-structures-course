import sys, queue

class StackWithMax:
    def __init__(self):
        self.stack = []
        self.maximums = []
    
    def push(self, value):
        self.stack.append(value)
        max_value = value if len(self.maximums) == 0 or self.maximums[-1] < value else self.maximums[-1]
        self.maximums.append(max_value)

    def pop(self):
        self.maximums.pop()
        return self.stack.pop()

    def max(self):
        return self.maximums[-1]

def main():
    stack = StackWithMax()
    reader = (s for s in sys.stdin)
    n = int(next(reader))
    for _ in range(n):
        splitted = next(reader).split()
        if splitted[0] == "push":
            stack.push(int(splitted[1]))
        elif splitted[0] == "pop":
            stack.pop()
        else:
            res = stack.max()
            print(res)

def generate_test_data():
    import random
    n = 4 * 10**5
    return [f'push {i}' for i in range(0, n // 2)] + \
        [random.choice(['pop', 'max', f'push {i}']) for i in range(0, n // 2)]

def generate_test_file(data):
    from utils import generate_test_file as generate
    generate('stack_with_max_test.txt', [f'{len(data)}\n'] + [f'{comm}\n' for comm in data])

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else None
    if(mode == 'generate'):
        generate_test_file(generate_test_data())
    else: 
        from utils import timed_min
        print(timed_min(main, n_iter=1))
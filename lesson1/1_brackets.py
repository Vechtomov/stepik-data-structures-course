def brackets(s):
    opened = []
    closing_brackets = {'}': '{', ')': '(', ']': '['}
    opening_brackets = ['(', '{', '[']
    for i, ch in enumerate(s):
        if ch in closing_brackets: 
            if len(opened) == 0 or opened.pop()[0] != closing_brackets[ch]: 
                return i
        elif ch in opening_brackets: 
            opened.append((ch, i))
    return -1 if len(opened) == 0 else opened.pop()[1]

def main():
    result = brackets(input())
    print("Success" if result < 0 else result + 1)

def test():
    from utils import are_equal
    method = brackets
    print("tests start")
    are_equal(method(""), -1)
    are_equal(method("a"), -1)
    are_equal(method("()"), -1)
    are_equal(method("(a)"), -1)
    are_equal(method("[]"), -1)
    are_equal(method("{}"), -1)
    are_equal(method("(())"), -1)
    are_equal(method("({})"), -1)
    are_equal(method("("), 0)
    are_equal(method(")("), 0)
    are_equal(method(")"), 0)
    are_equal(method("))"), 0)
    are_equal(method("(("), 1)
    are_equal(method("(()"), 0)
    are_equal(method("()("), 2)
    are_equal(method("())"), 2)
    are_equal(method("()))"), 2)
    are_equal(method("({[})"), 3)
    are_equal(method("a({[})"), 4)
    are_equal(method("([](){([])})"), -1)
    are_equal(method("()[]}"), 4)
    are_equal(method("{{[()]]"), 6)
    are_equal(method("({[([{}])]})"), -1)
    are_equal(method("(\n)"), -1)
    are_equal(method("(\n("), 2)
    are_equal(method("([]]()"), 3)
    are_equal(method("([]"), 0)
    are_equal(method("{{{**[][][]"), 2)
    are_equal(method("{{{**}[][][]"), 1)
    are_equal(method("[{(*)]"), 5)
    are_equal(method("({[})"), 3)
    are_equal(method("{}([]"), 2)
    are_equal(method("([](){([])})"), -1)
    print('all tests succeeded')

def performance():
    from utils import timed_min
    data = generate_test_data()
    generate_test_file(data)
    print(timed_min(brackets, data, n_iter=2))
    
def generate_test_data():
    import random
    return random.randint(1, 10**5)

def generate_test_file(data):
    from utils import generate_test_file as generate
    generate('brackets_test.txt', [f'{data}\n'])

if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else None
    if(mode == 'performance'): performance()
    elif(mode == 'test'): test()
    else: 
        from utils import timed_min
        print(timed_min(main, n_iter=1))
import sys

def solve(commands):
    book = {}
    for c in commands:
        if c[0] == 'add':
            book[c[1]] = c[2]
        elif c[0] == 'find':
            print(book[c[1]] if c[1] in book else 'not found')
        else:
            if c[1] in book:
                del book[c[1]]

def main():
    reader = (s for s in sys.stdin)
    n = int(next(reader))
    commands = [next(reader).split() for _ in range(n)]
    solve(commands)

if __name__ == "__main__":
    main()
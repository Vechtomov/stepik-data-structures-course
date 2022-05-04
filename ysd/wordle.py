from collections import defaultdict


def check(expected, actual, predict):
    result = ['W'] * 5
    d = defaultdict(int)
    for c in expected:
        d[c] += 1

    for i, c in enumerate(actual):
        if c == expected[i]:
            result[i] = 'G'
            d[c] -= 1
    
    y = defaultdict(int)
    for i, c in enumerate(actual):
        if result[i] == 'G':
            continue
        if c in d:
            result[i] = 'Y'
            if d[c] > 0:
                d[c] -= 1
                y[c] += 1

    r = True
    for i, c in enumerate(predict):
        a = result[i]
        s = actual[i]
        if a == 'G' and c != a:
            r = False
            break
        if c == 'G':
            if a != 'G':
                r = False
                break
        elif c == 'Y':
            if s not in d or s not in y or y[s] < 1:
                r = False
                break
            y[s] -= 1

    return sum(y.values()), r, ''.join(result), d, y

def game():
    expected = input()
    n = int(input())
    tries = [[None, None] for i in range(n)]
    result = ''
    for i in range(n):
        tries[i][0] = input()
    for i in range(n):
        tries[i][1] = input()
        r = check(expected, tries[i][0], tries[i][1])
        result += 'Y' if r[0] == 0 and r[1] else 'N'
    return result

def main():
    games = int(input())
    for i in range(games):
        r = game()
        print(r)
        if i < games - 1:
            input()

if __name__ == '__main__':
    main()
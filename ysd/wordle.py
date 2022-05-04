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
        if c == 'G':
            if a != 'G':
                r = False
                break
        elif c == 'W':
            if s not in d and a != 'W':
                r = False
                break
        else: # c = 'Y'
            if s not in d or s not in y or y[s] < 1:
                r = False
                break
            y[s] -= 1

    return sum(y.values()), r, ''.join(result), d, y

def game():
    expected = input()
    # print(expected)
    n = int(input())
    # print(n)
    tries = [[None, None] for i in range(n)]
    result = ''
    for i in range(n):
        tries[i][0] = input()
    # print(tries)
    for i in range(n):
        tries[i][1] = input()
        # print(tries)
        r = check(expected, tries[i][0], tries[i][1])
        # print(r)
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
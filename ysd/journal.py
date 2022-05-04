
def get_next_date(date):
    y, m, d = date
    if m == 12 and d == 31:
        return (y + 1, 1, 1)
    elif d == 30 and (m == 4 or m == 6 or m == 9 or m == 11):
        return (y, m + 1, 1)
    elif d == 31 and (m == 1 or m == 3 or m == 5 or m == 7 or m == 8 or m == 10):
        return (y, m + 1, 1)
    elif d == 28 and m == 2:
        return (y, m if y % 4 == 0 else m + 1, d + 1 if y % 4 == 0 else 1)
    elif d == 29 and m == 2:
        return (y, m + 1, 1)
    else:
        return (y, m, d + 1)


def main():
    n, *_ = map(int, input().split())
    arr = [0] * n
    for i in range(n):
        d, m, y = map(int, input().split('-'))
        arr[i] = (y, m, d)
    arr.sort()
    max_sequence = 1
    curr_sequence = 1
    last_date = arr[0]
    for date in arr:
        next_date = get_next_date(last_date)
        if date == last_date:
            continue
        if date == next_date:
            curr_sequence += 1
        else:
            curr_sequence = 1
        max_sequence = max(max_sequence, curr_sequence)
        last_date = date
    return max_sequence


if __name__ == '__main__':
    print(main())

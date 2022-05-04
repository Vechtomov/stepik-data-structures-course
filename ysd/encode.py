def main():
    s = input()
    codes = []
    curr = ''
    chars = set()
    for i in range(len(s)):
        if s[i].isalpha():
            num = int(curr) if curr != '' else 1
            curr = ''
            chars.add(s[i])
            codes.append((s[i], num))
        else:
            curr += s[i]

    return codes


if __name__ == '__main__':
    print(main())

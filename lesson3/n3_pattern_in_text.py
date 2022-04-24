class Hash:
    def __init__(self, q=1_000_000_007, x=263) -> None:
        self.q = q
        self.x = x
        self.powers = [1]

    def __call__(self, string) -> int:
        res = 0
        q = self.q
        for i, ch in enumerate(string):
            xi = self._x_pow(len(string) - i - 1)
            res = (res + (ord(ch)*xi) % q) % q
        return res

    def get_new_hash(self, string_len, old_sym, new_sym, old_hash):
        q = self.q
        x1 = self._x_pow(1)
        xn = self._x_pow(string_len-1)
        return ((((old_hash - (ord(old_sym)*xn) % q)) % q * x1) % q + ord(new_sym)) % q

    def _x_pow(self, i):
        q = self.q
        while i >= len(self.powers):
            self.powers.append((self.powers[-1] * self.x % q) % q)
        return self.powers[i]


def solve(text, pattern):
    assert len(text) >= len(pattern)
    result = []
    h = Hash(x=101)
    p_hash = h(pattern)
    curr_str = ''
    for i, c in enumerate(text):
        if i < len(pattern) - 1:
            curr_str += c
            continue
        elif i == len(pattern) - 1:
            curr_str += c
            curr_str_hash = h(curr_str)
        else:
            curr_str_hash = h.get_new_hash(
                len(curr_str), curr_str[0], c, curr_str_hash)
            curr_str = curr_str[1:] + c
        if p_hash == curr_str_hash and pattern == curr_str:
            result.append(i - len(pattern) + 1)

    return result


def main():
    pattern = input()
    text = input()
    res = solve(text, pattern)
    print(' '.join(map(str, res)))


if __name__ == "__main__":
    main()

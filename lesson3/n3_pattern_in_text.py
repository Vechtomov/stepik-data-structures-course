class Hash:
    def __init__(self, m, p=1_000_000_007, x=263) -> None:
        self.m = m
        self.p = p
        self.x = x
        self.powers = [1]

    def __call__(self, string) -> int:
        res = 0
        for i, ch in enumerate(string):
            res = (res + ord(ch)*self._x_pow(i)) % self.p
        return res % self.m

    def _x_pow(self, i):
        while i >= len(self.powers):
            self.powers.append((self.powers[-1] * self.x % self.p) % self.p)
        return self.powers[i]


def solve(text, pattern):
    assert len(text) >= len(pattern)
    result = []
    h = Hash(5)
    p_hash = h(pattern)
    curr_str = ''
    for i, c in enumerate(text):
        if i < len(pattern) - 1:
            curr_str += c
            continue
        elif i == len(pattern) - 1:
            curr_str += c
        else:
            curr_str = curr_str[1:] + c
        t_hash = h(curr_str)
        if p_hash == t_hash and pattern == curr_str:
            result.append(i - len(pattern) + 1)

    return result


def main():
    pattern = input()
    text = input()
    res = solve(text, pattern)
    print(' '.join(map(str, res)))


if __name__ == "__main__":
    main()

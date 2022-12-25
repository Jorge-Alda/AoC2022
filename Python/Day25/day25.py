from pathlib import Path

basepath = Path(__file__).parent

SNAFU = {"0": 0, "1": 1, "2": 2, "-": -1, "=": -2}
rev_SNAFU = {0: "0", 1: "1", 2: "2", -1: "-", -2: "="}


def from_SNAFU(s: str) -> int:
    return sum(SNAFU[k]*5**i for i, k in enumerate(reversed(s)))


def to_SNAFU(x0: int) -> str:
    x = x0
    res = ""
    while x != 0:
        rem = x % 5
        if rem > 2:
            rem = rem - 5
        res = rev_SNAFU[rem] + res
        x = (x - rem) // 5
    return res


def part1(inp: str) -> str:
    return to_SNAFU(sum(from_SNAFU(x) for x in inp.splitlines()))


if __name__ == "__main__":
    with open(basepath/"input", "rt") as f:
        inp = f.read()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

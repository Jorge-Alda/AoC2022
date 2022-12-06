from pathlib import Path

basepath = Path(__file__).parent


def part1(inp: str) -> int:
    for i in range(len(inp)-4):
        s = set(inp[i:i+4])
        if len(s) == 4:
            return i+4
    raise ValueError


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

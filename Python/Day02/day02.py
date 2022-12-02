import itertools
from enum import Enum
from pathlib import Path

basepath = Path(__file__).parent


class PlayElf(int, Enum):
    A = 1  # Rock
    B = 2  # Paper
    C = 3  # Scissors


class PlayHuman(int, Enum):
    X = 1  # Rock
    Y = 2  # Paper
    Z = 3  # Scissors


def scores() -> dict[str, int]:
    d = {}
    for e, h in itertools.product("ABC", "XYZ"):
        res = (PlayHuman[h] - PlayElf[e]) % 3
        score_points = {0: 3, 1: 6, 2: 0}
        d.update({" ".join((e, h)): PlayHuman[h]+score_points[res]})
    return d


def part1(inp: str) -> int:
    score_table = scores()
    return sum(score_table[m] for m in inp.split('\n'))


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

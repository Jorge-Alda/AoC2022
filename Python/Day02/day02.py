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


class ResultHuman(int, Enum):
    X = 2  # Lose
    Y = 0  # Draw
    Z = 1  # Win


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


def part2(inp: str) -> int:
    tot = 0
    score_table = scores()
    for m in inp.split('\n'):
        e = m[0]
        h = m[2]
        playcode = (PlayElf[e] + ResultHuman[h]) % 3
        play = PlayHuman(playcode if playcode > 0 else 3)
        tot += score_table[" ".join((e, play.name))]
    return tot

if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

    out2 = part2(inp)
    with open(basepath/"output2", "wt") as f:
        f.write(str(out2))

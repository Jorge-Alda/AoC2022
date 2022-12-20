from day20 import part1, part2
from pathlib import Path

basepath = Path(__file__).parent


def test_part1():
    with open(basepath/"test", "rt") as f:
        inp = f.read().strip()
    res = part1(inp)
    assert res == 3


def test_part2():
    with open(basepath/"test", "rt") as f:
        inp = f.read().strip()
    res = part2(inp)
    assert res == 1623178306

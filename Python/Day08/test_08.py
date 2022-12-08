from day08 import part1, part2
from pathlib import Path

basepath = Path(__file__).parent


def test_part1():
    with open(basepath/"test", "rt") as f:
        inp = f.read().strip()
    out = part1(inp)
    assert out == 21


def test_part2():
    with open(basepath/"test", "rt") as f:
        inp = f.read().strip()
    out = part2(inp)
    assert out == 8

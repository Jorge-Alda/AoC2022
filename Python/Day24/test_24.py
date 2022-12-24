from day24 import part1, part2
from pathlib import Path

basepath = Path(__file__).parent


def test_part1():
    with open(basepath/"test", "rt") as f:
        inp = f.read()

    res = part1(inp, show=True)
    assert res == 18


def test_part2():
    with open(basepath/"test", "rt") as f:
        inp = f.read()

    res = part2(inp, show=True)
    assert res == 54

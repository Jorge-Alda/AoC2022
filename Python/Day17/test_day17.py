from day17 import part1, part2
from pathlib import Path

basepath = Path(__file__).parent


def test_part1_1():
    with open(basepath/"test", "rt") as f:
        inp = f.read().strip()
    out = part1(inp, 1)
    assert out == 1


def test_part1_2():
    with open(basepath/"test", "rt") as f:
        inp = f.read().strip()
    out = part1(inp, 2)
    assert out == 4


def test_part1_3():
    with open(basepath/"test", "rt") as f:
        inp = f.read().strip()
    out = part1(inp, 3)
    assert out == 6


def test_part1_4():
    with open(basepath/"test", "rt") as f:
        inp = f.read().strip()
    out = part1(inp, 4)
    assert out == 7


def test_part1():
    with open(basepath/"test", "rt") as f:
        inp = f.read().strip()
    out = part1(inp, 2022)
    assert out == 3068


def test_part2():
    with open(basepath/"test", "rt") as f:
        inp = f.read().strip()
    out = part2(inp, 1_000_000_000_000)
    assert out == 1_514_285_714_288

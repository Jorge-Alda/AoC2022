from day15 import part1, part2, Interval
from pathlib import Path

basepath = Path(__file__).parent


def test_part1():
    with open(basepath/"test", "rt") as f:
        inp = f.read().strip()
    out = part1(inp, 10)
    assert out == 26


def test_part2():
    with open(basepath/"test", "rt") as f:
        inp = f.read().strip()
    out = part2(inp, 20)
    assert out == 56000011


def test_interval():
    i1 = Interval.new(9, 11)
    i2 = Interval.new(10, 13)
    itot = Interval.new(9, 13)
    assert (i1 | i2) == itot

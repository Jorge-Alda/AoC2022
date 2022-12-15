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

class TestIntervals:
    @staticmethod
    def test_disjoint():
        i1 = Interval.new(1, 7)
        i2 = Interval.new(10, 13)
        ires = i1 | i2
        assert str(ires) == "[1, 7], [10, 13]"


    @staticmethod
    def test_overlap():
        i1 = Interval.new(9, 11)
        i2 = Interval.new(10, 13)
        ires = i1 | i2
        itot = Interval.new(9, 13)
        assert ires == itot


    @staticmethod
    def test_multiple():
        i1 = Interval.new(1, 3) | Interval.new(11, 13)
        i2 = Interval.new(2, 7) | Interval.new(9, 13)
        itot = i1 | i2
        assert str(itot) == "[1, 7], [9, 13]"

    @staticmethod
    def test_coincidence():
        i1 = Interval.new(1, 2) | Interval.new(2, 3)
        i2 = Interval.new(1, 3)
        assert i1 == i2

    @staticmethod
    def test_merge():
        i1 = Interval.new(1, 2) | Interval.new(3, 4)
        i2 = Interval.new(1, 4)
        assert i1 == i2

    @staticmethod
    def test_inter_contained():
        i1 = Interval.new(1, 10) & Interval.new(4, 5)
        i2 = Interval.new(4, 5)
        assert i1 == i2

    @staticmethod
    def test_inter_overlap():
        i1 = Interval.new(1, 10) & Interval.new(7, 13)
        i2 = Interval.new(7, 10)
        assert i1 == i2

    @staticmethod
    def test_inter_coincidence():
        i1 = Interval.new(1, 10) & Interval.new(7, 10)
        i2 = Interval.new(7, 10)
        assert i1 == i2

    @staticmethod
    def test_inter_union():
        i1 = Interval.new(1, 5) | Interval.new(8, 11)
        i2 = i1 & Interval.new(3, 10)
        i3 = Interval.new(3, 5) | Interval.new(8, 10)
        assert i2 == i3

    @staticmethod
    def test_inter_mulunion():
        i1 = Interval.new(1, 5) | Interval.new(8, 15)
        i2 = Interval.new(3, 10) | Interval.new(13, 21)
        ires = i1 & i2
        i3 = Interval.new(3, 5) | Interval.new(8, 10) | Interval.new(13, 15)
        assert ires == i3

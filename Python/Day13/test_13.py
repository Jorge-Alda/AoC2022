from day13 import Result, compare, part1
from pathlib import Path

basepath = Path(__file__).parent


def test_compare():
    assert compare([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]) == Result.Left
    assert compare([[1], [2, 3, 4]], [[1], 4]) == Result.Left
    assert compare([9], [[8, 7, 6]]) == Result.Right
    assert compare([[4, 4], 4, 4], [[4, 4], 4, 4, 4]) == Result.Left
    assert compare([7, 7, 7, 7], [7, 7, 7]) == Result.Right
    assert compare([], [3]) == Result.Left
    assert compare([[[]]], [[]]) == Result.Right
    assert compare([1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [
                   1, [2, [3, [4, [5, 6, 0]]]], 8, 9]) == Result.Right


def test_part1():
    with open(basepath/"test", "rt") as f:
        inp = f.read().strip()
    out = part1(inp)
    assert out == 13

from day23 import part1
from pathlib import Path

basepath = Path(__file__).parent


def test_part1():
    with open(basepath/"test", "rt") as f:
        inp = f.read()

    res = part1(inp)
    assert res == 110

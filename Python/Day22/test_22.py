from day22 import solve
from pathlib import Path

basepath = Path(__file__).parent


def test_part1():
    with open(basepath/"test", "rt") as f:
        inp = f.read()
    res = solve(inp, 1)
    assert res == 6032

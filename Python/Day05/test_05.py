from day05 import part1
from pathlib import Path

basepath = Path(__file__).parent


def test_part1():
    with open(basepath/"test", "rt") as f:
        inp = f.read()
    out = part1(inp)
    assert out == "CMZ"

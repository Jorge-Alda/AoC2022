from day25 import from_SNAFU, to_SNAFU, part1
from pathlib import Path

basepath = Path(__file__).parent


def test_from_SNAFU():
    assert from_SNAFU("1=-1=") == 353
    assert from_SNAFU("1121-1110-1=0") == 314159265


def test_to_SNAFU():
    assert to_SNAFU(12345) == "1-0---0"


def test_part1():
    with open(basepath/"test", "rt") as f:
        inp = f.read()

    res = part1(inp)
    assert res == "2=-1=0"

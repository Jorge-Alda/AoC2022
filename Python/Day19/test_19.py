from day19 import part1, Blueprint
from pathlib import Path

basepath = Path(__file__).parent


def test_quality():
    with open(basepath/"test", "rt") as f:
        inp = f.read().strip()
    bps = (Blueprint(l.strip()) for l in inp.splitlines())
    qualys = [bp.quality(24) for bp in bps]
    assert qualys == [9, 24]


def test_part1():
    with open(basepath/"test", "rt") as f:
        inp = f.read().strip()
    out = part1(inp)
    assert out == 33

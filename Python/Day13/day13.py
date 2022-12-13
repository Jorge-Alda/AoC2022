from enum import Enum
from pathlib import Path

basepath = Path(__file__).parent


class Result(Enum):
    Left = 0
    Right = 1
    Undecided = 2


def compare(left: int | list, right: int | list) -> Result:
    match (left, right):
        case (int(l), int(r)):
            if l < r:
                return Result.Left
            elif l == r:
                return Result.Undecided
            else:
                return Result.Right
        case (int(l), list(r)):
            return compare([l,], r)
        case (list(l), int(r)):
            return compare(l, [r,])
        case (list(ll), list(rr)):
            for l, r in zip(ll, rr):
                res = compare(l, r)
                if res == Result.Left or res == Result.Right:
                    return res
            if len(ll) < len(rr):
                return Result.Left
            elif len(ll) > len(rr):
                return Result.Right
            else:
                return Result.Undecided
        case _:
            raise ValueError


def part1(inp: str) -> int:
    tot = 0
    pairs = inp.split('\n\n')
    for i, p in enumerate(pairs):
        l, r = p.split('\n')
        left = eval(l)
        right = eval(r)
        if compare(left, right) == Result.Left:
            tot += i+1
    return tot


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

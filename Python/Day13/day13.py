from enum import Enum
from pathlib import Path
from functools import cmp_to_key

basepath = Path(__file__).parent


class Result(Enum):
    Left = 0
    Right = 1
    Undecided = 2

    def to_int(self) -> int:
        if self == Result.Left:
            return -1
        if self == Result.Undecided:
            return 0
        else:
            return 1


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


def part2(inp: str) -> int:
    packets = [[[2]], [[6]]]
    for l in inp.split('\n'):
        if l != "":
            packets.append(eval(l))
    packets.sort(key=cmp_to_key(lambda x, y: compare(x, y).to_int()))
    pos_2 = packets.index([[2]]) + 1
    pos_6 = packets.index([[6]]) + 1
    return pos_2 * pos_6


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

    out2 = part2(inp)
    with open(basepath/"output2", "wt") as f:
        f.write(str(out2))

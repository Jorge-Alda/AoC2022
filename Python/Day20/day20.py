from typing import TypeVar, Generic
from pathlib import Path

basepath = Path(__file__).parent

T = TypeVar("T")


class Element(Generic[T]):
    def __init__(self, val: T, left: int, right: int) -> None:
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"({self.val}: {self.left}, {self.right})"


def to_dllist(l: list[T]) -> list[Element[T]]:
    len_l = len(l)
    lefts = [len_l-1] + list(range(len_l-1))
    rights = list(range(1, len_l)) + [0]
    return [Element(*x) for x in zip(l, lefts, rights)]


def move_right(l: list[Element], pos: int, num: int = 0):
    for _ in range(num % (len(l)-1)):
        right = l[pos].right
        rright = l[right].right
        left = l[pos].left
        l[left].right, l[pos].right, l[right].right = l[pos].right, l[right].right, l[left].right
        l[pos].left, l[right].left, l[rright].left = l[rright].left, l[pos].left, l[right].left


def move_left(l: list[Element], pos: int, num: int = 0):
    for _ in range(num % (len(l)-1)):
        left = l[pos].left
        lleft = l[left].left
        right = l[pos].right
        l[right].left, l[pos].left, l[left].left = l[pos].left, l[left].left, l[right].left
        l[pos].right, l[left].right, l[lleft].right = l[lleft].right, l[pos].right, l[left].right


def move(l: list[Element], pos: int, num: int = 0):
    if num > 0:
        move_right(l, pos, num)
    if num < 0:
        move_left(l, pos, -num)


def transverse_right(l: list[Element[T]], pos: int, num: int) -> T:
    for _ in range(num):
        pos = l[pos].right
    return l[pos].val


def part1(inp: str) -> int:
    parsed = [int(l) for l in inp.splitlines()]
    dlinked = to_dllist(parsed)
    pos_0 = 0
    for i in range(len(dlinked)):
        move(dlinked, i, dlinked[i].val)
        if dlinked[i].val == 0:
            pos_0 = i
    return transverse_right(dlinked, pos_0, 1000) + transverse_right(dlinked, pos_0, 2000) + transverse_right(dlinked, pos_0, 3000)


def part2(inp: str) -> int:
    key = 811589153
    parsed = [int(l)*key for l in inp.splitlines()]
    dlinked = to_dllist(parsed)
    pos_0 = 0
    for _ in range(10):
        for i in range(len(dlinked)):
            move(dlinked, i, dlinked[i].val)
            if dlinked[i].val == 0:
                pos_0 = i
    return transverse_right(dlinked, pos_0, 1000) + transverse_right(dlinked, pos_0, 2000) + transverse_right(dlinked, pos_0, 3000)

if __name__ == "__main__":
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

    out2 = part2(inp)
    with open(basepath/"output2", "wt") as f:
        f.write(str(out2))

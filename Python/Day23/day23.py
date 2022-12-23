from typing import Self
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

basepath = Path(__file__).parent


@dataclass(unsafe_hash=True)
class Point:
    x: int = field(hash=True)
    y: int = field(hash=True)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, rhs: Self) -> Self:
        return Point(self.x + rhs.x, self.y + rhs.y)


def parse(inp: str) -> list[Point]:
    elfs: list[Point] = []
    for y, l in enumerate(inp.splitlines()):
        for x, c in enumerate(l):
            if c == "#":
                elfs.append(Point(x, y))
    return elfs


def round(elfs: list[Point], round_n: int) -> list[Point]:
    neighbors = [Point(1, 0), Point(1, 1), Point(
        0, 1), Point(-1, 1), Point(-1, 0), Point(-1, -1), Point(0, -1), Point(1, -1)]
    neighbors_dir = [
        [Point(0, -1), Point(1, -1), Point(-1, -1)],
        [Point(0, 1), Point(1, 1), Point(-1, 1)],
        [Point(-1, 0), Point(-1, 1), Point(-1, -1)],
        [Point(1, 0), Point(1, 1), Point(1, -1)]
    ]
    new_elfs: list[Point] = []
    candidates: Counter[Point] = Counter()
    move_to: dict[Point, Point] = {}
    for p in elfs:
        set_n = {p+n for n in neighbors}
        occupied = set(elfs) & set_n
        if len(occupied) == 0:
            new_elfs.append(p)
        else:
            for i in range(4):
                dir = (round_n + i) % 4
                if not any((p+n) in elfs for n in neighbors_dir[dir]):
                    candidates[p + neighbors_dir[dir][0]] += 1
                    move_to[p] = p + neighbors_dir[dir][0]
                    break
            else:
                new_elfs.append(p)
    for p in move_to.keys():
        if candidates[move_to[p]] == 1:
            new_elfs.append(move_to[p])
        else:
            new_elfs.append(p)
    return new_elfs


def part1(inp: str) -> int:
    elfs = parse(inp)
    for i in range(10):
        elfs = round(elfs, i)
    min_x = min(e.x for e in elfs)
    max_x = max(e.x for e in elfs)
    min_y = min(e.y for e in elfs)
    max_y = max(e.y for e in elfs)
    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(elfs)


if __name__ == "__main__":
    with open(basepath/"input", "rt") as f:
        inp = f.read()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

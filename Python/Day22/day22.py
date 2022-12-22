import re
from enum import Enum
from typing import Self
from collections import defaultdict
from pathlib import Path

basepath = Path(__file__).parent

Point = tuple[int, int]


class Direction(int, Enum):
    Right = 0
    Down = 1
    Left = 2
    Up = 3

    def turn_R(self) -> Self:
        return Direction((self.value + 1) % 4)

    def turn_L(self) -> Self:
        return Direction((self.value - 1) % 4)

    def turn(self, dir: str) -> Self:
        match dir:
            case "L":
                return self.turn_L()
            case "R":
                return self.turn_R()
            case _:
                raise ValueError

    def __repr__(self) -> str:
        match self:
            case Direction.Up:
                return "^"
            case Direction.Right:
                return ">"
            case Direction.Down:
                return "v"
            case Direction.Left:
                return "<"


def score(p: Point) -> int:
    return 1000 * (p[1]+1) + 4 * (p[0] + 1)


def parse(inp: str) -> tuple[list[int], list[str], defaultdict[Point, dict[Direction, Point]]]:
    raw_map, raw_moves = tuple(inp.split('\n\n'))
    moves = list(reversed([int(m) for m in re.findall(r"[0-9]+", raw_moves)]))
    turns = list(reversed(re.findall(r"[LR]", raw_moves)))
    dict_map: defaultdict[Point, dict[Direction, Point]] = defaultdict(dict)
    for y, l in enumerate(raw_map.splitlines()):
        m = re.match(r"(\s*)([.#]+)", l)
        if m is not None:
            blanks = len(m.group(1))
            full_line = m.group(2)
            for x in range(len(full_line)):
                if full_line[x] == ".":
                    if x == 0:
                        left = len(full_line) - 1
                    else:
                        left = x - 1
                    if full_line[left] == ".":
                        dict_map[(x + blanks, y)
                                 ] |= {Direction.Left: (left + blanks, y)}
                    if x == len(full_line) - 1:
                        right = 0
                    else:
                        right = x + 1
                    if full_line[right] == ".":
                        dict_map[(x + blanks, y)
                                 ] |= {Direction.Right: (right + blanks, y)}
    max_l = max(len(l) for l in raw_map.splitlines())
    trans_lines = [f"{l:<{max_l}}" for l in raw_map.splitlines()]
    transposed = ["".join(list(k)).rstrip() for k in zip(*trans_lines)]
    for x, l in enumerate(transposed):
        m = re.match(r"(\s*)([.#]+)", l)
        if m is not None:
            blanks = len(m.group(1))
            full_line = m.group(2)
            for y in range(len(full_line)):
                if full_line[y] == ".":
                    if y == 0:
                        up = len(full_line) - 1
                    else:
                        up = y - 1
                    if full_line[up] == ".":
                        dict_map[(x, y + blanks)
                                 ] |= {Direction.Up: (x, up + blanks)}
                    if y == len(full_line) - 1:
                        down = 0
                    else:
                        down = y + 1
                    if full_line[down] == ".":
                        dict_map[((x, y + blanks))
                                 ] |= {Direction.Down: (x, down + blanks)}
    return moves, turns, dict_map


def part1(inp: str) -> int:
    moves, turns, dict_map = parse(inp)
    pos = min(dict_map.keys(), key=score)
    facing = Direction.Right
    while len(turns) > 0:
        moving = moves.pop()
        for _ in range(moving):
            pos = dict_map[pos].get(facing, pos)
        facing = facing.turn(turns.pop())
    moving = moves.pop()
    for _ in range(moving):
        pos = dict_map[pos].get(facing, pos)
    return score(pos) + facing.value


if __name__ == "__main__":
    with open(basepath/"input", "rt") as f:
        inp = f.read()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

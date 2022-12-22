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


def parse(inp: str) -> tuple[list[int], list[str], defaultdict[Point, dict[Direction, tuple[Point, Direction]]]]:
    raw_map, raw_moves = tuple(inp.split('\n\n'))
    moves = list(reversed([int(m) for m in re.findall(r"[0-9]+", raw_moves)]))
    turns = list(reversed(re.findall(r"[LR]", raw_moves)))
    dict_map: defaultdict[Point, dict[Direction,
                                      tuple[Point, Direction]]] = defaultdict(dict)
    for y, l in enumerate(raw_map.splitlines()):
        m = re.match(r"(\s*)([.#]+)", l)
        if m is not None:
            blanks = len(m.group(1))
            full_line = m.group(2)
            for x in range(len(full_line)):
                if full_line[x] == ".":
                    if x == 0:
                        xf = len(full_line) - 1 + blanks
                        yf = y
                        f = Direction.Left
                    else:
                        xf = x - 1 + blanks
                        yf = y
                        f = Direction.Left
                    if raw_map.splitlines()[yf][xf] == ".":
                        dict_map[(x + blanks, y)
                                 ] |= {Direction.Left: ((xf, y), f)}
                    if x == len(full_line) - 1:
                        xf = blanks
                        yf = y
                        f = Direction.Right
                    else:
                        xf = x + 1 + blanks
                        yf = y
                        f = Direction.Right
                    if raw_map.splitlines()[yf][xf] == ".":
                        dict_map[(x + blanks, y)
                                 ] |= {Direction.Right: ((xf, yf), f)}
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
                        yf = len(full_line) - 1 + blanks
                        xf = x
                        f = Direction.Up
                    else:
                        yf = y - 1 + blanks
                        xf = x
                        f = Direction.Up
                    if raw_map.splitlines()[yf][xf] == ".":
                        dict_map[(x, y + blanks)
                                 ] |= {Direction.Up: ((xf, yf), f)}
                    if y == len(full_line) - 1:
                        yf = blanks
                        xf = x
                        f = Direction.Down
                    else:
                        yf = y + 1 + blanks
                        xf = x
                        f = Direction.Down
                    if raw_map.splitlines()[yf][xf] == ".":
                        dict_map[((x, y + blanks))
                                 ] |= {Direction.Down: ((xf, yf), f)}
    return moves, turns, dict_map


def part1(inp: str) -> int:
    moves, turns, dict_map = parse(inp)
    pos = min(dict_map.keys(), key=score)
    facing = Direction.Right
    while len(turns) > 0:
        moving = moves.pop()
        for _ in range(moving):
            pos, facing = dict_map[pos].get(facing, (pos, facing))
        facing = facing.turn(turns.pop())
    moving = moves.pop()
    for _ in range(moving):
        pos, facing = dict_map[pos].get(facing, (pos, facing))
    return score(pos) + facing.value


if __name__ == "__main__":
    with open(basepath/"input", "rt") as f:
        inp = f.read()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

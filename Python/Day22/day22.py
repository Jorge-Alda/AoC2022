#!/usr/bin/env python

import re
from enum import Enum
from typing import Self
from collections import defaultdict
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from time import sleep

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


def parse(inp: str, part: int) -> tuple[list[int], list[str], defaultdict[Point, dict[Direction, tuple[Point, Direction]]]]:
    raw_map, raw_moves = tuple(inp.split('\n\n'))
    moves = list(reversed([int(m) for m in re.findall(r"[0-9]+", raw_moves)]))
    turns = list(reversed(re.findall(r"[LR]", raw_moves)))
    dict_map: defaultdict[Point, dict[Direction,
                                      tuple[Point, Direction]]] = defaultdict(dict)
    for y, l in enumerate(raw_map.splitlines()):
        m = re.match(r"(\s*)([.#]+)", l)
        if m is None:
            raise ValueError
        blanks = len(m.group(1))
        full_line = m.group(2)
        for x in range(len(full_line)):
            if full_line[x] == ".":
                if x == 0 and part == 1:
                    xf = len(full_line) - 1 + blanks
                    yf = y
                    f = Direction.Left
                elif x == 0 and part > 1:
                    if y < 50:
                        xf = 0
                        yf = 149 - y
                        f = Direction.Right
                    elif y < 100:
                        xf = y - 50
                        yf = 100
                        f = Direction.Down
                    elif y < 150:
                        xf = 50
                        yf = 149 - y
                        f = Direction.Right
                    else:
                        xf = y - 100
                        yf = 0
                        f = Direction.Down
                else:
                    xf = x - 1 + blanks
                    yf = y
                    f = Direction.Left
                if raw_map.splitlines()[yf][xf] == ".":
                    dict_map[(x + blanks, y)
                             ] |= {Direction.Left: ((xf, y), f)}
                if x == len(full_line) - 1 and part == 1:
                    xf = blanks
                    yf = y
                    f = Direction.Right
                elif x == len(full_line) - 1 and part > 1:
                    if y < 50:
                        xf = 99
                        yf = 149 - y
                        f = Direction.Left
                    elif y < 100:
                        xf = y + 50
                        yf = 49
                        f = Direction.Up
                    elif y < 150:
                        xf = 149
                        yf = 149 - y
                        f = Direction.Left
                    else:
                        xf = y - 100
                        yf = 149
                        f = Direction.Up
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
        if m is None:
            raise ValueError
        blanks = len(m.group(1))
        full_line = m.group(2)
        for y in range(len(full_line)):
            if full_line[y] == ".":
                if y == 0 and part == 1:
                    yf = len(full_line) - 1 + blanks
                    xf = x
                    f = Direction.Up
                elif y == 0 and part > 1:
                    if x < 50:
                        xf = 50
                        yf = x + 50
                        f = Direction.Right
                    elif x < 100:
                        xf = 0
                        yf = x + 100
                        f = Direction.Right
                    else:
                        xf = x - 100
                        yf = 199
                        f = Direction.Up
                else:
                    yf = y - 1 + blanks
                    xf = x
                    f = Direction.Up
                if raw_map.splitlines()[yf][xf] == ".":
                    dict_map[(x, y + blanks)
                             ] |= {Direction.Up: ((xf, yf), f)}
                if y == len(full_line) - 1 and part == 1:
                    yf = blanks
                    xf = x
                    f = Direction.Down
                elif y == len(full_line) - 1 and part > 1:
                    if x < 50:
                        xf = x + 100
                        yf = 0
                        f = Direction.Down
                    elif x < 100:
                        xf = 49
                        yf = 100 + x
                        f = Direction.Left
                    else:
                        xf = 99
                        yf = x - 50
                        f = Direction.Left
                else:
                    yf = y + 1 + blanks
                    xf = x
                    f = Direction.Down
                if raw_map.splitlines()[yf][xf] == ".":
                    dict_map[((x, y + blanks))
                             ] |= {Direction.Down: ((xf, yf), f)}
    return moves, turns, dict_map


def solve(inp: str, part: int, show: bool = True) -> int:
    plt.ion()
    moves, turns, dict_map = parse(inp, part)
    pos = min(dict_map.keys(), key=score)
    facing = Direction.Right
    max_y = max(p[1] for p in dict_map.keys())
    while len(turns) > 0:
        moving = moves.pop()
        for _ in range(moving):
            pos, facing = dict_map[pos].get(facing, (pos, facing))
            if show:
                plt.gcf().clear()
                for p in dict_map.keys():
                    plt.scatter(p[0], max_y - p[1], c="lightgray", marker=".")
                plt.scatter(pos[0], max_y - pos[1],
                            c="green", marker=repr(facing))
                for p, _ in dict_map[pos].values():
                    plt.scatter(p[0], max_y - p[1], c="red", marker="o")
                plt.pause(0.5)
                plt.gcf().canvas.flush_events()
        facing = facing.turn(turns.pop())
    moving = moves.pop()
    for _ in range(moving):
        pos, facing = dict_map[pos].get(facing, (pos, facing))
    return score(pos) + facing.value


if __name__ == "__main__":
    with open(basepath/"input", "rt") as f:
        inp = f.read()

    out1 = solve(inp, 1)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

    #out2 = solve(inp, 2)
    # with open(basepath/"output2", "wt") as f:
    #    f.write(str(out2))

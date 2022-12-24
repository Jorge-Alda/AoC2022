from math import lcm
from collections import defaultdict
from pathlib import Path
import matplotlib.pyplot as plt

basepath = Path(__file__).parent


class Blizzard:
    def __init__(self, dim_x: int, dim_y: int,
                 blizzards_N: list[tuple[int, int]],
                 blizzards_S: list[tuple[int, int]],
                 blizzards_E: list[tuple[int, int]],
                 blizzards_W: list[tuple[int, int]]) -> None:
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.period = lcm(dim_x-2, dim_y-2)
        self.pattern_N = [blizzards_N]
        self.pattern_S = [blizzards_S]
        self.pattern_E = [blizzards_E]
        self.pattern_W = [blizzards_W]
        self.visited: defaultdict[tuple[int, int],
                                  list[int]] = defaultdict(list)
        for i in range(self.period-1):
            self.pattern_N.append(move_blizzards_N(dim_y, self.pattern_N[i]))
            self.pattern_S.append(move_blizzards_S(dim_y, self.pattern_S[i]))
            self.pattern_E.append(move_blizzards_E(dim_x, self.pattern_E[i]))
            self.pattern_W.append(move_blizzards_W(dim_x, self.pattern_W[i]))

    def check_walls(self, pos: tuple[int, int]) -> bool:
        return (pos == (1, self.dim_y-1)) or (pos == (self.dim_x-2, 0)) or ((pos[0] > 0) and (pos[0] < self.dim_x-1) and (pos[1] > 0) and (pos[1] < self.dim_y-1))

    def check_blizz(self, pos: tuple[int, int], turn: int) -> bool:
        return pos not in self.pattern_N[(turn+1) % self.period] and pos not in self.pattern_S[(turn+1) % self.period] and pos not in self.pattern_E[(turn+1) % self.period] and pos not in self.pattern_W[(turn+1) % self.period]

    def run(self, pos: tuple[int, int], show: bool = False) -> int:
        candidates = [pos]
        turn = 0
        while 1:
            next_c = []
            if show:
                self.plot(turn, candidates)
            for p0 in candidates:
                if p0 == (self.dim_x-2, 0):
                    return turn
                if any((turn-x) % self.period == 0 for x in self.visited[p0]):
                    continue
                self.visited[p0].append(turn)
                neighbors = [p0,
                             (p0[0], p0[1]+1),
                             (p0[0], p0[1]-1),
                             (p0[0]+1, p0[1]),
                             (p0[0]-1, p0[1])
                             ]
                for p in neighbors:
                    if self.check_walls(p) and self.check_blizz(p, turn):
                        next_c.append(p)
            candidates = next_c
            turn += 1
        return -1

    def plot(self, turn: int, candidates: list[tuple[int, int]]):
        coords_x = [c[0]+0.01 for c in candidates]
        coords_y = [c[1]+0.01 for c in candidates]
        blizzN_x = [c[0] for c in self.pattern_N[turn % self.period]]
        blizzN_y = [c[1] for c in self.pattern_N[turn % self.period]]
        blizzS_x = [c[0] for c in self.pattern_S[turn % self.period]]
        blizzS_y = [c[1] for c in self.pattern_S[turn % self.period]]
        blizzE_x = [c[0] for c in self.pattern_E[turn % self.period]]
        blizzE_y = [c[1] for c in self.pattern_E[turn % self.period]]
        blizzW_x = [c[0] for c in self.pattern_W[turn % self.period]]
        blizzW_y = [c[1] for c in self.pattern_W[turn % self.period]]
        plt.gcf().clear()
        plt.xlim(-0.2, self.dim_x-0.8)
        plt.ylim(-0.2, self.dim_y-0.8)
        plt.scatter(blizzN_x, blizzN_y, c="lightgray", marker="^")
        plt.scatter(blizzS_x, blizzS_y, c="lightgray", marker="v")
        plt.scatter(blizzE_x, blizzE_y, c="lightgray", marker=">")
        plt.scatter(blizzW_x, blizzW_y, c="lightgray", marker="<")
        plt.axhline(0)
        plt.axhline(self.dim_y-1)
        plt.axvline(0)
        plt.axvline(self.dim_x-1)
        plt.scatter(coords_x, coords_y, c="red", marker=".")
        plt.title(f"t={turn}")
        plt.pause(0.1)
        plt.gcf().canvas.flush_events()


def parse(inp: str) -> Blizzard:
    plt.ion()
    blizzards_N: list[tuple[int, int]] = []
    blizzards_S: list[tuple[int, int]] = []
    blizzards_E: list[tuple[int, int]] = []
    blizzards_W: list[tuple[int, int]] = []
    lines = inp.splitlines()
    dim_y = len(lines)
    dim_x = len(lines[0])
    lines.pop()
    for i in range(len(lines) - 1):
        line = lines.pop()
        for j, c in enumerate(line):
            if c == "^":
                blizzards_N.append((j, i+1))
            elif c == "v":
                blizzards_S.append((j, i+1))
            elif c == "<":
                blizzards_W.append((j, i+1))
            elif c == ">":
                blizzards_E.append((j, i+1))
    return Blizzard(dim_x, dim_y, blizzards_N, blizzards_S, blizzards_E, blizzards_W)


def move_blizzards_N(dim_y: int, blizzards: list[tuple[int, int]]) -> list[tuple[int, int]]:
    new_blizzards: list[tuple[int, int]] = []
    # There is no ^ blizzards in the first or last columns, so they can't block the entrance or exit
    for b in blizzards:
        if b[1] < dim_y-2:
            new_blizzards.append((b[0], b[1]+1))
        else:
            new_blizzards.append((b[0], 1))
    return new_blizzards


def move_blizzards_S(dim_y: int, blizzards: list[tuple[int, int]]) -> list[tuple[int, int]]:
    new_blizzards: list[tuple[int, int]] = []
    # There is no v blizzards in the first or last columns, so they can't block the entrance or exit
    for b in blizzards:
        if b[1] > 1:
            new_blizzards.append((b[0], b[1]-1))
        else:
            new_blizzards.append((b[0], dim_y-2))
    return new_blizzards


def move_blizzards_E(dim_x: int, blizzards: list[tuple[int, int]]) -> list[tuple[int, int]]:
    new_blizzards: list[tuple[int, int]] = []
    for b in blizzards:
        if b[0] < dim_x-2:
            new_blizzards.append((b[0]+1, b[1]))
        else:
            new_blizzards.append((1, b[1]))
    return new_blizzards


def move_blizzards_W(dim_x: int, blizzards: list[tuple[int, int]]) -> list[tuple[int, int]]:
    new_blizzards: list[tuple[int, int]] = []
    for b in blizzards:
        if b[0] > 1:
            new_blizzards.append((b[0]-1, b[1]))
        else:
            new_blizzards.append((dim_x-2, b[1]))
    return new_blizzards


def part1(inp: str, show: bool = False) -> int:
    bliz = parse(inp)
    return bliz.run((1, bliz.dim_y-1), show)


if __name__ == "__main__":
    with open(basepath/"input", "rt") as f:
        inp = f.read()

    out1 = part1(inp, True)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

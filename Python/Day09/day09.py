from enum import Enum
from pathlib import Path
from copy import deepcopy

basepath = Path(__file__).parent


class Movement(Enum):
    Up = "U"
    Down = "D"
    Right = "R"
    Left = "L"


def move(m: Movement, pos: tuple[int, int]) -> tuple[int, int]:
    match m:
        case Movement.Up:
            return (pos[0], pos[1]+1)
        case Movement.Down:
            return (pos[0], pos[1]-1)
        case Movement.Right:
            return (pos[0]+1, pos[1])
        case Movement.Left:
            return (pos[0]-1, pos[1])


def delta(x: int) -> int:
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1

class Rope:
    def __init__(self, knots=1):
        self.n_knots = knots
        self.coords: list[tuple[int, int]] = [(0, 0) for _ in range(knots+1)]

    def move_rope(self, m: Movement):
        old_pos = deepcopy(self.coords)
        self.coords[0] = move(m, self.coords[0])

        for k in range(1, self.n_knots+1):
            relpos = (self.coords[k-1][0] - self.coords[k][0],
                      self.coords[k-1][1] - self.coords[k][1])
            if relpos[0]**2+relpos[1]**2 <= 2:
                pass

            else:
                x = self.coords[k][0] + delta(relpos[0])
                y = self.coords[k][1] + delta(relpos[1])
                self.coords[k] = (x, y)



def parse(inp: str) -> list[Movement]:
    moves = []
    for l in inp.split('\n'):
        direction, num = l.split(' ')
        moves += [Movement(direction)]*int(num)
    return moves


def part1(inp: str) -> int:
    positions = {(0, 0)}
    rope = Rope()
    for m in parse(inp):
        rope.move_rope(m)
        positions |= {rope.coords[-1]}
    return len(positions)


def part2(inp: str) -> int:
    positions = {(0, 0)}
    rope = Rope(9)
    for m in parse(inp):
        rope.move_rope(m)
        positions |= {rope.coords[-1]}
    return len(positions)


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

    out2 = part2(inp)
    with open(basepath/"output2", "wt") as f:
        f.write(str(out2))

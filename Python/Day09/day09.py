from enum import Enum
from pathlib import Path

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


class Rope:
    def __init__(self):
        self.H = (0, 0)
        self.T = (0, 0)

    @property
    def length(self) -> int:
        return (self.H[0]-self.T[0])**2 + (self.H[1]-self.T[1])**2

    def move_rope(self, m: Movement):
        old_H = self.H
        self.H = move(m, self.H)

        lnew = self.length
        if lnew < 4:
            pass
        elif lnew == 4:
            self.T = move(m, self.T)
        else:
            self.T = old_H


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
        positions |= {rope.T}
    return len(positions)


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

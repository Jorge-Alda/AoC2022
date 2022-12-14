from itertools import pairwise
from pathlib import Path

basepath = Path(__file__).parent


def parse_rocks(inp: str) -> set[tuple[int, int]]:
    rocks = set()
    for l in inp.split('\n'):
        for s, e in pairwise(l.split(" -> ")):
            start = tuple(int(i) for i in s.split(','))
            end = tuple(int(i) for i in e.split(','))
            if start[0] != end[0]:
                minx, maxx = sorted((start[0], end[0]))
                rocks |= set((x, start[1]) for x in range(minx, maxx+1))
            else:
                miny, maxy = sorted((start[1], end[1]))
                rocks |= set((start[0], y) for y in range(miny, maxy+1))
    return rocks


def drop_sand(rocks: set[tuple[int, int]]) -> bool:
    pos = [500, 0]
    abyss = max(r[1] for r in rocks)
    while 1:
        if pos[1] > abyss:
            return False
        if (pos[0], pos[1]+1) not in rocks:
            pos[1] += 1
        elif (pos[0]-1, pos[1]+1) not in rocks:
            pos[0] -= 1
            pos[1] += 1
        elif (pos[0]+1, pos[1]+1) not in rocks:
            pos[0] += 1
            pos[1] += 1
        else:
            rocks.add(tuple(pos))
            break
    return True


def part1(inp: str) -> int:
    sand = 0
    rocks = parse_rocks(inp)
    while drop_sand(rocks):
        sand += 1
    return sand


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

from pathlib import Path

basepath = Path(__file__).parent


def dist(p1: tuple[int, int, int], p2: tuple[int, int, int]) -> int:
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) + abs(p1[2]-p2[2])


def part1(inp: str) -> int:
    cubes = []
    surface = 0
    for c in inp.splitlines():
        cube = tuple(int(x) for x in c.split(','))
        surface += 6 - sum(2 for t in cubes if dist(cube, t) == 1)
        cubes.append(cube)
    return surface


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

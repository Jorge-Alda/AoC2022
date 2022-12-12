from pathlib import Path

basepath = Path(__file__).parent


def parse(inp: str) -> tuple[list[list[int]], tuple[int, int], tuple[int, int]]:
    lines = inp.split('\n')
    lenx = len(lines)
    leny = len(lines[0])
    (sx, sy) = (0, 0)
    (ex, ey) = (0, 0)
    hmap = [[0 for _ in range(leny)] for _ in range(lenx)]
    for x, l in enumerate(lines):
        for y, c in enumerate(l):
            if c == 'S':
                sx = x
                sy = y
                hmap[x][y] = 0
            elif c == 'E':
                ex = x
                ey = y
                hmap[x][y] = ord('z') - ord('a')
            else:
                hmap[x][y] = ord(c) - ord('a')
    return hmap, (sx, sy), (ex, ey)


def part1(inp: str) -> int:
    hmap, start, end = parse(inp)
    lenx = len(hmap)
    leny = len(hmap[0])
    candidates = [start]
    visited = {start}
    steps = 0
    stop = False
    while 1:
        new = []
        for p in candidates:
            for np in [(p[0]-1, p[1]), (p[0]+1, p[1]), (p[0], p[1]-1), (p[0], p[1]+1)]:
                if np[0] in range(lenx) and np[1] in range(leny) and np not in visited and hmap[np[0]][np[1]] - hmap[p[0]][p[1]] <= 1:
                    if np == end:
                        stop = True
                    new.append(np)
                    visited |= {np}
        steps += 1
        if stop:
            break
        candidates = new
    return steps


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

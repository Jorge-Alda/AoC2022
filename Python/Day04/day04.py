from pathlib import Path

basepath = Path(__file__).parent


def part1(inp: str) -> int:
    overlaps = 0
    for l in inp.split('\n'):
        elf1, elf2 = l.split(',')
        start1, end1 = elf1.split('-')
        start2, end2 = elf2.split('-')
        if (int(start1) <= int(start2)) and (int(end1) >= int(end2)):
            overlaps += 1
        elif (int(start1) >= int(start2)) and (int(end1) <= int(end2)):
            overlaps += 1
    return overlaps


def part2(inp: str) -> int:
    overlaps = 0
    for l in inp.split('\n'):
        elf1, elf2 = l.split(',')
        start1, end1 = elf1.split('-')
        start2, end2 = elf2.split('-')
        if (int(end1) >= int(start2)) and (int(end2) >= int(start1)):
            overlaps += 1
    return overlaps


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

    out2 = part2(inp)
    with open(basepath/"output2", "wt") as f:
        f.write(str(out2))

from pathlib import Path

basepath = Path(__file__).parent


def part1(inp: str) -> int:
    overlaps = 0
    for l in inp.split('\n'):
        elf1, elf2 = l.split(',')
        start1, end1 = elf1.split('-')
        start2, end2 = elf2.split('-')
        if (int(start1) <= int(start2)) and (int(end1) >= int(end2)):
            print(f"1>2: {l}")
            overlaps += 1
        elif ((s1 := int(start1)) >= (s2 := int(start2))) and ((e1 := int(end1)) <= (e2 := int(end2))):
            print(f"2>1: {l}")
            overlaps += 1
    return overlaps


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

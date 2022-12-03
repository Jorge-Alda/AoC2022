from pathlib import Path

basepath = Path(__file__).parent


def part1(inp: str) -> int:
    tot = 0
    for rucksack in inp.split('\n'):
        l = int(len(rucksack)/2)
        comp1 = rucksack[:l]
        comp2 = rucksack[l:]
        for it in comp1:
            if it in comp2:
                p = ord(it)
                if p > 96:
                    priority = (p-96)
                else:
                    priority = (p-38)
                tot += priority
                break
    return tot


def part2(inp: str) -> int:
    tot = 0
    rucksacks = inp.split('\n')
    for i in range(int(len(rucksacks)/3)):
        r1 = rucksacks[3*i]
        r2 = rucksacks[3*i+1]
        r3 = rucksacks[3*i+2]
        for it in r1:
            if it in r2:
                if it in r3:
                    p = ord(it)
                    if p > 96:
                        priority = (p-96)
                    else:
                        priority = (p-38)
                    tot += priority
                    break
    return tot


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

    out2 = part2(inp)
    with open(basepath/"output2", "wt") as f:
        f.write(str(out2))

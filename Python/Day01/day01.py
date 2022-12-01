def part1(inp: str) -> int:
    elfs = []
    calories = 0
    for l in inp.split('\n'):
        if l == "":
            elfs.append(calories)
            calories = 0
        else:
            calories += int(l)
    return max(elfs)


if __name__ == '__main__':
    print("Starting")
    with open('Python/Day01/status', 'wt') as f:
        f.write("0")

    print("Part 1")
    with open('Python/Day01/input', 'rt') as f:
        inp = f.read()

    out1 = part1(inp)
    with open('Python/Day01/output1', 'wt') as f:
        f.write(str(out1))

    with open('Python/Day01/status', 'wt') as f:
        f.write("1")

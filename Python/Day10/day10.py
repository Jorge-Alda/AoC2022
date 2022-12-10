from pathlib import Path

basepath = Path(__file__).parent


def part1(inp: str) -> int:
    cycles = 0
    X = 1
    strengths = []
    target_cycle = 20
    for command in inp.split('\n'):
        instruction = command[:4]
        cycles += 1
        if instruction == 'addx':
            cycles += 1
        if cycles >= target_cycle:
            strengths.append(X * target_cycle)
            target_cycle += 40
        if instruction == 'addx':
            X += int(command[5:])
    return sum(strengths)


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

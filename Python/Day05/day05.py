from pathlib import Path

basepath = Path(__file__).parent


def parse_input(inp: str) -> tuple[list[str], list[str]]:
    cr, instructions = inp.split('\n\n')
    cr_s = cr.split('\n')
    crates = cr_s[:-1]
    containers = cr_s[-1]
    num = int(containers.split()[-1])

    crate_list = ['' for _ in range(num)]
    for c in crates:
        for i in range(num):
            ind = 4*i+1
            if len(c) > ind:
                x = c[4*i+1]
                if x != ' ':
                    crate_list[i] += x

    return (crate_list, instructions.strip().split('\n'))


def rev(s: str) -> str:
    return "".join(list(reversed(s)))


def part1(inp: str) -> str:
    crates, instructions = parse_input(inp)
    print(crates)
    for ins in instructions:
        ins_s = ins.split()
        quant = int(ins_s[1])
        source = int(ins_s[3])-1
        dest = int(ins_s[5])-1
        crates[dest] = str(rev(crates[source][:quant])) + crates[dest]
        crates[source] = crates[source][quant:]
    return "".join(c[0] for c in crates)


def part2(inp: str) -> str:
    crates, instructions = parse_input(inp)
    for ins in instructions:
        ins_s = ins.split()
        quant = int(ins_s[1])
        source = int(ins_s[3])-1
        dest = int(ins_s[5])-1
        crates[dest] = crates[source][:quant] + crates[dest]
        crates[source] = crates[source][quant:]
    return "".join(c[0] for c in crates)

if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

    out2 = part2(inp)
    with open(basepath/"output2", "wt") as f:
        f.write(str(out2))

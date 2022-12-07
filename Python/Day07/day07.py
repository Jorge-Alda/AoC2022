from pathlib import Path

basepath = Path(__file__).parent


def parent(directory: str) -> str:
    return "/".join(directory.split("/")[:-1])


def child(path: str, directory: str) -> str:
    return path + '/' + directory


def dir_tree(directory: str) -> list[str]:
    tree = []
    dirs = directory.split('/')
    for i in range(len(dirs)+1):
        tree.append("/".join(dirs[0:i]))
    return tree


def filesystem(inp: str) -> dict[str, int]:
    files = {'': 0}
    cwd = ''
    tree = ['']
    for l in inp.split('\n')[1:]:
        if l == "$ cd ..":
            cwd = parent(cwd)
            tree = dir_tree(cwd)
        elif l[:5] == "$ cd ":
            cwd = child(cwd, l[5:])
            tree = dir_tree(cwd)
        elif l[:4] == "dir ":
            files.update({child(cwd, l[4:]): 0})
        elif l[0] != '$':
            size = int(l.split(' ')[0])
            for d in tree:
                files[d] += size
    return files


def part1(inp: str) -> int:
    fs = filesystem(inp)
    return sum(v for v in fs.values() if v <= 100000)


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

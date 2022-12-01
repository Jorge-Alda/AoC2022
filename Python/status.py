"""Adapted from
* https://gitlab.com/JeroenStiers/advent-of-code-2022/-/blob/d1f52588aa89a494945ed9ce7a4ef628f8d3b323/new_day.py
* https://github.com/Starwort/aoc_helper/blob/88c03b6cdba632d39e66f2b3be269ff361fba5f0/aoc_helper/interface.py
"""

import datetime
from pathlib import Path
import requests
import browser_cookie3
import re
from markdownify import markdownify

YEAR = 2022

start_date = datetime.date(YEAR, 11, 30)
today = datetime.date.today()

try:
    with open("../ua", "rt") as f:
        useragent = f.read()
    headers = {'User-Agent': useragent}
except:
    headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0"}


def create_dir(path: Path):
    if not path.exists():
        path.mkdir()
        with open(path/"status", "wt") as f:
            f.write("0")
        with open(path/".gitignore", "wt") as f:
            f.write("input\noutput1\noutput2")


def get_puzzle(path: Path, day: int):
    cookie = browser_cookie3.firefox(domain_name="adventofcode.com")
    req = requests.get(
        f"https://adventofcode.com/{YEAR}/day/{day}", cookies=cookie, headers=headers)
    with open(path/"README.md", "wt") as f:
        for g in re.finditer(pattern=r"(<article[\S\s]*?<\/article>)", string=req.text):
            g2 = re.match(
                r'<article class="day-desc"><h2>--- ([\S\s]*?) ---</h2>([\S\s]*?</article>)', g.group(0))
            if g2 is not None:
                text = f'<article class="day-desc"><h1>{g2.groups()[0]}</h1>{g2.groups()[1]}'
            else:
                g3 = re.match(
                    r'<article class="day-desc"><h2 id="part2">--- Part Two ---</h2>([\S\s]*?</article>)', g.group(0))
                if g3 is not None:
                    text = f'<article class="day-desc"><h2 id="part2">Part Two</h2>{g3.groups()[0]}'
                else:
                    text = g.group(0)
            f.write(markdownify(text.replace('<a href="/',
                    '<a href="https://adventofcode.com/')).replace('`*', '`').replace('*`', '`'))

def get_input(path: Path, day: int):
    cookie = browser_cookie3.firefox(domain_name="adventofcode.com")
    req = requests.get(
        f"https://adventofcode.com/{YEAR}/day/{day}/input", cookies=cookie, headers=headers)
    with open(path/"input", "wt") as f:
        f.write(req.text)


def submit(path: Path, day: int, part: str) -> bool:
    cookie = browser_cookie3.firefox(domain_name="adventofcode.com")
    with open(path/f"output{part}", "rt") as f:
        answer = f.read()
    print(f"Checking day {day:02d} part {part}")
    resp = requests.post(f"https://adventofcode.com/{YEAR}/day/{day}/answer",
                         cookies=cookie,
                         data={"level": part, "answer": answer},
                         headers=headers)
    g = re.match(r'[\S\s]*?(<p>[\S\s]*?</p>)', resp.text)
    if g:
        print(g.groups()[0][3:-4])
        return g.groups()[0].startswith("<p>That's the")
    return False


if __name__ == '__main__':
    with open("README.md", "wt") as f:
        f.write("# Advent of Code 2022 - Python 🐍\n\n")
        if today > start_date:
            f.write("AoC already started!\n\n")
            delta = today - start_date
            days = min(delta.days, 25)
            puzzles = 0
            complete_days = 0
            for i in range(1, days+1):
                f.write(f"* [Day {i:02d}](Day{i:02d})")
                path = Path(".")/f"Day{i:02}"
                if path.exists():
                    with open(path/"status", "rt") as fs:
                        status = fs.read()
                    if status == '2':
                        f.write("🟩\n")
                        puzzles += 2
                        complete_days += 1
                    elif status == '1':
                        if (path/"output2").exists() and submit(path, i, "2"):
                                f.write("🟩\n")
                                puzzles += 2
                                complete_days += 1
                                with open(path/"status", "wt") as fs:
                                    fs.write("2")
                        else:
                            f.write("🟨\n")
                            puzzles += 1
                    else:
                        if (path/"output1").exists() and submit(path, i, "1"):
                                f.write("🟨\n")
                                puzzles += 1
                                get_puzzle(path, i)
                                with open(path/"status", "wt") as fs:
                                    fs.write("1")
                        else:
                            f.write("🟥\n")
                else:
                    f.write("🟦\n")
                    create_dir(path)
                    get_puzzle(path, i)
                    get_input(path, i)
            f.write(
                f"\nPuzzles completed: {puzzles}/{2*days} ({50*puzzles/days:.2f}%)")
            f.write(
                f"\nDays completed: {complete_days}/{days} ({100*complete_days/days:.2f}%)\n")
        else:
            delta = start_date - today
            f.write(
                f"AoC hasn't started yet. It will start in {delta.days + 1} days!\n")

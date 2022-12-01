"""Adapted from https://gitlab.com/JeroenStiers/advent-of-code-2022/-/blob/d1f52588aa89a494945ed9ce7a4ef628f8d3b323/new_day.py"""

import datetime
from pathlib import Path
import requests
import browser_cookie3
import re
from markdownify import markdownify

YEAR = 2022
start_date = datetime.date(YEAR, 11, 30)
today = datetime.date.today()


def create_dir(path: Path):
    if not path.exists():
        path.mkdir()
        with open(path/"status") as f:
            f.write("0")
        with open(path/".gitignore") as f:
            f.write("target\ninput\n\output1\noutput2")


def get_input(path: Path, day: int):
    cookie = browser_cookie3.firefox(domain_name="adventofcode.com")
    req = requests.get(
        f"https://adventofcode.com/{YEAR}/day/{day}/input", cookies=cookie)
    with open(path/"input", "wt") as f:
        f.write(req.text)


def get_puzzle(path: Path, day: int):
    cookie = browser_cookie3.firefox(domain_name="adventofcode.com")
    req = requests.get(
        f"https://adventofcode.com/{YEAR}/day/{day}", cookies=cookie)
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


if __name__ == '__main__':
    if today > start_date:
        delta = today - start_date
        d = min(delta.days, 25)
        path_python = Path(f"./Python/Day{d:02d}")
        path_rust = Path(f"./Rust/day{d:02d}")
        for p in (path_python, path_rust):
            create_dir(p)
            get_input(p, d)
            get_puzzle(p, d)

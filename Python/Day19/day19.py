import re
from enum import Enum
from copy import deepcopy
from pathlib import Path
from multiprocessing import Pool
from pathlib import Path

basepath = Path(__file__).parent

# Adapted from https://github.com/deivi-drg/advent-of-code-2022/blob/main/Day19/day19.py

basepath = Path(__file__).parent


class Robots(Enum):
    Ore = 0
    Clay = 1
    Obs = 2
    Geo = 3


class Blueprint:
    def __init__(self, command: str):
        pattern = r"Blueprint ([0-9]*): Each ore robot costs ([0-9]*) ore. Each clay robot costs ([0-9]*) ore. Each obsidian robot costs ([0-9]*) ore and ([0-9]*) clay. Each geode robot costs ([0-9]*) ore and ([0-9]*) obsidian."
        m = re.match(pattern, command)
        if m is None:
            raise ValueError
        self.idn = int(m.group(1))
        self.orer_cost = int(m.group(2))
        self.clayr_cost = int(m.group(3))
        self.obsr_cost_ore = int(m.group(4))
        self.obsr_cost_clay = int(m.group(5))
        self.geor_cost_ore = int(m.group(6))
        self.geor_cost_obs = int(m.group(7))

    @property
    def max_ore_cost(self) -> int:
        return max([self.orer_cost, self.clayr_cost, self.geor_cost_ore, self.obsr_cost_ore])

    def quality(self, time: int) -> int:
        m = Mining(self, time)
        m.next_step({})
        return self.idn * m.max_geo


class Mining:
    def __init__(self,
                 bp: Blueprint,
                 time: int,
                 ore_robots: int = 1,
                 clay_robots: int = 0,
                 obs_robots: int = 0,
                 geo_robots: int = 0,
                 ore: int = 0,
                 clay: int = 0,
                 obs: int = 0,
                 geo: int = 0,
                 max_geo=0):
        self.bp = bp
        self.time = time
        self.ore_robots = ore_robots
        self.clay_robots = clay_robots
        self.obs_robots = obs_robots
        self.geo_robots = geo_robots
        self.ore = ore
        self.clay = clay
        self.obs = obs
        self.geo = geo
        self.max_geo = max_geo

    def update_mats(self):
        self.ore += self.ore_robots
        self.clay += self.clay_robots
        self.obs += self.obs_robots
        self.geo += self.geo_robots

    def purchase_robot(self, robot: Robots):
        match robot:
            case Robots.Ore:
                self.ore_robots += 1
                self.ore -= self.bp.orer_cost
            case Robots.Clay:
                self.clay_robots += 1
                self.ore -= self.bp.clayr_cost
            case Robots.Obs:
                self.obs_robots += 1
                self.ore -= self.bp.obsr_cost_ore
                self.clay -= self.bp.obsr_cost_clay
            case Robots.Geo:
                self.geo_robots += 1
                self.obs -= self.bp.geor_cost_obs
                self.ore -= self.bp.geor_cost_ore

    def enough_mats(self) -> list[Robots]:
        enough: list[Robots] = []
        if (self.ore >= self.bp.geor_cost_ore) and (self.obs >= self.bp.geor_cost_obs):
            enough.append(Robots.Geo)
        if (self.obs_robots < self.bp.geor_cost_obs) and (self.ore >= self.bp.obsr_cost_ore) and (self.clay >= self.bp.obsr_cost_clay):
            enough.append(Robots.Obs)
        if (self.clay_robots < self.bp.obsr_cost_clay) and (self.ore >= self.bp.clayr_cost):
            enough.append(Robots.Clay)
        if (self.ore_robots < self.bp.max_ore_cost) and (self.ore >= self.bp.orer_cost):
            enough.append(Robots.Ore)
        return enough

    def achievable(self) -> int:
        return self.geo_robots*self.time + (self.time * (self.time - 1))//2

    def next_step(self, cache: dict[tuple[int, ...], int]) -> dict[tuple[int, ...], int]:
        cached = (self.time, self.ore, self.clay, self.obs, self.geo,
                  self.ore_robots, self.clay_robots, self.obs_robots, self.geo_robots)
        if cached in cache:
            self.max_geo = cache[cached]
            return cache
        if self.geo + self.achievable() <= self.max_geo:
            return cache
        to_purchase = self.enough_mats()
        self.update_mats()
        if self.time == 1:
            self.max_geo = self.geo
            return cache
        no_purchase = deepcopy(self)
        no_purchase.time -= 1
        cache = no_purchase.next_step(cache)
        geo = no_purchase.max_geo
        self.max_geo = max(geo, self.max_geo)
        for robot in to_purchase:
            candidate = deepcopy(self)
            candidate.purchase_robot(robot)
            candidate.time -= 1
            cache = candidate.next_step(cache)
            geo = candidate.max_geo
            self.max_geo = max(geo, self.max_geo)
        cache |= {cached: self.max_geo}
        return cache


def qualy(bp: Blueprint) -> int:
    return bp.quality(24)


def max_geo(bp: Blueprint) -> int:
    m = Mining(bp, 32)
    m.next_step({})
    return m.max_geo


def part1(inp: str) -> int:
    bps = (Blueprint(l.strip()) for l in inp.splitlines())

    with Pool() as pool:
        q = pool.map(qualy, bps)

    return sum(q)


def part2(inp: str) -> int:
    bps = [Blueprint(l.strip()) for _, l in zip([0, 1, 2], inp.splitlines())]

    with Pool(processes=3) as pool:
        q = pool.map(max_geo, bps)

    return q[0] * q[1] * q[2]


if __name__ == '__main__':
    with open(basepath/"input", "rt") as f:
        inp = f.read().strip()

    out1 = part1(inp)
    with open(basepath/"output1", "wt") as f:
        f.write(str(out1))

    out2 = part2(inp)
    with open(basepath/"output2", "wt") as f:
        f.write(str(out2))

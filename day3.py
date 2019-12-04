import re
import time
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, NamedTuple, Tuple

from lib.utils import readdata_csv, timestamp

nodepattern: re.Pattern = re.compile(r"(?P<direction>\w)(?P<length>\d+)")


class Direction(Enum):
    Up = "U"
    Down = "D"
    Left = "L"
    Right = "R"


class Point(NamedTuple):
    x: int
    y: int


@dataclass
class Cursor():
    p: Point

    def __init__(self, x, y):
        self.p = Point(x, y)

    def step(self, direction: Direction):
        if direction == Direction.Up:
            self.p = Point(self.p.x, self.p.y + 1)
        elif direction == Direction.Right:
            self.p = Point(self.p.x + 1, self.p.y)
        elif direction == Direction.Down:
            self.p = Point(self.p.x, self.p.y - 1)
        elif direction == Direction.Left:
            self.p = Point(self.p.x - 1, self.p.y)

    @property
    def point(self) -> Point:
        return self.p


@dataclass
class Wire():
    wireid: int
    dist: int


@dataclass
class Junction():
    location: Point
    wires: List[Wire]

    @property
    def manhattan_dist(self) -> int:
        return abs(self.location.x) + abs(self.location.y)

    @property
    def pathlen(self) -> int:
        x: Wire
        return sum(x.dist for x in self.wires)


class Board:
    wiremap: Dict[Point, Wire]
    numwires = 0

    def __init__(self, paths):
        self.wiremap = {}
        for path in paths:
            self.drawpath(path)

    def drawpath(self, path):
        self.numwires += 1
        pathid = self.numwires
        cursor = Cursor(0, 0)
        totalDist = 0
        for node in path:
            d, length = self.parsenode(node)
            for _ in range(length):
                totalDist += 1
                cursor.step(d)
                p = cursor.point
                if p not in self.wiremap:
                    self.wiremap[p] = []

                x: Wire
                selfcross = [x for x in self.wiremap[p] if x.wireid == pathid]
                if not selfcross:
                    self.wiremap[p].append(Wire(pathid, totalDist))

    def parsenode(self, node) -> Tuple[str, str]:
        result = nodepattern.match(node)
        groups = result.groupdict()
        return Direction(groups["direction"]), int(groups["length"])

    @property
    def junctions(self) -> List[Junction]:
        k: Point
        v: List[Wire]
        junctions = [Junction(k, v) for k, v in self.wiremap.items() if len(v) > 1]
        return junctions

    def get_best_manhattan_dist(self):
        closest: Junction = min(self.junctions, key=lambda j: j.manhattan_dist)
        return closest.manhattan_dist

    def get_best_pathlen(self):
        closest: Junction = min(self.junctions, key=lambda j: j.pathlen)
        return closest.pathlen


def get_best_mdist(paths):
    b = Board(paths)
    return b.get_best_manhattan_dist()


def get_best_path(paths):
    b = Board(paths)
    return b.get_best_pathlen()


def test():
    # part 1 tests
    d0a = "R8,U5,L5,D3".split(",")
    d0b = "U7,R6,D4,L4".split(",")
    r0 = get_best_mdist([d0a, d0b])
    assert r0 == 6

    d1a = "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(",")
    d1b = "U62,R66,U55,R34,D71,R55,D58,R83".split(',')
    r1 = get_best_mdist([d1a, d1b])
    assert r1 == 159

    d2a = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(",")
    d2b = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(",")
    r2 = get_best_mdist([d2a, d2b])
    assert r2 == 135

    # Part 2 tests
    r2 = get_best_path([d1a, d1b])
    assert r2 == 610

    assert get_best_path([d2a, d2b]) == 410

# test()


def part1(paths):
    return get_best_mdist(paths)


def part2(paths):
    return get_best_path(paths)


data = readdata_csv("day3.csv")

start = time.time()
p1result = part1(data)
timestamp(start, f"Part 1: {p1result}")

start = time.time()
p2result = part2(data)
timestamp(start, f"Part 2: {p2result}")

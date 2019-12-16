import time
from itertools import cycle
from typing import Dict, Iterator, List, NamedTuple, Tuple

from lib.gfx import FracCoord, Point
from lib.utils import readdata, timestamp


class ObjectType(NamedTuple):
    Void = "."
    Asteroid = "#"
    LAZOR = "X"


class MapperHelper:
    @staticmethod
    def get_table_dimensions(table: List[List[str]]) -> Point:
        return Point(len(table[0]), len(table))

    @staticmethod
    def count_asteroids(table: List[List[str]]) -> int:
        return sum(line.count(ObjectType.Asteroid) for line in table)

    @staticmethod
    def generate_angle_table(size: Point):
        angles = []

        for y in range(size.y):
            for x in range(size.x):
                if x == y == 0:
                    continue
                angles.append(FracCoord(x, y))
                angles.append(FracCoord(x, -y))
                angles.append(FracCoord(-x, -y))
                angles.append(FracCoord(-x, y))

        angles = sorted(list(set(angles)))
        return angles


class Mapper(MapperHelper):
    size: Point
    zap_origin: Point
    scanner_angle: FracCoord
    asteroid_map: List[List[int]]
    num_asteroids = int
    angle_table: List[FracCoord]
    angle_iterator: Iterator[FracCoord]

    def __init__(self, data):
        self.scanner_angle = FracCoord(0, -1)
        self.zap_origin = Point(0, 0)

        self.size = self.get_table_dimensions(data)
        self.parse_map(data)

        self.angle_table = Mapper.generate_angle_table(self.size)
        self.angle_iterator: Iterator[FracCoord] = cycle(self.angle_table)

    def parse_map(self, data):
        self.asteroid_map = [[] * self.size.x] * self.size.y

        for y in range(self.size.y):
            if ObjectType.LAZOR in data[y]:
                self.zap_origin = Point(data[y].index(ObjectType.LAZOR), y)
            self.asteroid_map[y] = list(data[y])

        self.num_asteroids = Mapper.count_asteroids(self.asteroid_map)

    def has_asteroid(self, x, y):
        if not 0 <= x < self.size.x or not 0 <= y < self.size.y:
            return False
        return self.asteroid_map[y][x] == ObjectType.Asteroid

    def set_zap_origin(self, origin: Point):
        self.zap_origin = origin
        self.asteroid_map[origin.y][origin.x] = ObjectType.LAZOR
        self.num_asteroids = self.count_asteroids(self.asteroid_map)

    def trace(self, origin: Point, angle: FracCoord) -> Point:
        pt_x = origin.x + angle.x
        pt_y = origin.y + angle.y

        while 0 <= pt_x < self.size.x and 0 <= pt_y < self.size.y:
            if self.has_asteroid(pt_x, pt_y):
                return Point(pt_x, pt_y)
            pt_x += angle.x
            pt_y += angle.y

    def get_sweep_angles(self) -> List[FracCoord]:
        rotation_complete = False
        start_angle = self.scanner_angle
        while True:
            a: FracCoord = next(self.angle_iterator)
            if a == start_angle:
                if rotation_complete:
                    return a
                rotation_complete = True
            yield a

    def scan(self, origin: Point, sweep_once=False) -> Point:
        max_scans = len(self.angle_table)
        num_scans = 0
        while True:
            num_scans += 1
            self.scanner_angle = next(self.get_sweep_angles())
            hit = self.trace(origin, self.scanner_angle)
            if hit:
                yield hit
            if sweep_once and max_scans == num_scans or self.num_asteroids == 0:
                return

    def sweep(self, origin: Point) -> List[Point]:
        return [x for x in self.scan(origin=origin, sweep_once=True)]

    def zap(self, pt: Point):
        self.asteroid_map[pt.y][pt.x] = ObjectType.Void
        self.num_asteroids -= 1

    def zap_sweep(self, limit: int = 0, leave_alive: int = 0) -> List[Point]:
        killsheet = []
        while self.num_asteroids > leave_alive and limit and len(killsheet) < limit:
            hit = next(self.scan(self.zap_origin))
            self.zap(hit)
            killsheet.append(hit)
        return killsheet

    def zap_EVERYTHING(self) -> List[Point]:
        def zap(pt: Point):
            self.zap(pt)
            return pt
        killsheet = [zap(hit) for hit in self.scan(self.zap_origin)]
        return killsheet

    def get_visibility_table(self) -> Dict[Point, Point]:
        asteroids = []
        size = Mapper.get_table_dimensions(self.asteroid_map)

        for y in range(size.y):
            for x in range(size.x):
                pt = self.asteroid_map[y][x]

                if pt == ObjectType.Asteroid:
                    asteroids.append(Point(x, y))

        vistable = {}
        for astr in asteroids:
            vistable[astr] = [x for x in self.scan(astr, sweep_once=True)]

        return vistable

    def get_best_location(self) -> Tuple[Point, int]:
        vismap = self.get_visibility_table().items()
        vismap = {k: len(v) for k, v in vismap}
        best = max(vismap.items(), key=lambda x: x[1])
        return best


def part1(data):
    start = time.time()
    best_location = Mapper(data).get_best_location()
    timestamp(start, f"Part 1: {best_location}")


def part2(data):
    start = time.time()
    m = Mapper(data)
    m.set_zap_origin(FracCoord(23, 19))
    killsheet = m.zap_EVERYTHING()
    the_bet = killsheet[199]
    timestamp(start, f"Part 2: {the_bet.x*100 + the_bet.y}")


if __name__ == "__main__":
    testdata = readdata("day10.map")
    part1(testdata)
    part2(testdata)

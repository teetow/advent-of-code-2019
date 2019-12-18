import time
from collections import abc
from copy import deepcopy
from enum import IntEnum
from typing import Dict, NamedTuple

from lib.gfx import Point
from lib.intcoder import Intcoder, RunResult
from lib.utils import readnumbers_csv, timestamp


class MapToken(IntEnum):
    Void = -1
    Black = 0
    White = 1
    Robot = 99

    @property
    def symbol(self):
        return [".", "#", " "][int(self.value)]


class Turn(NamedTuple):
    Left = 0
    Right = 1


class Heading(IntEnum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3


class Paintmap(abc.MutableMapping):
    store: Dict

    def __init__(self):
        super().__init__()
        self.store: Dict[Point, MapToken] = {}

    def __setitem__(self, key: Point, value: MapToken):
        self.store[key] = value

    def __getitem__(self, key: Point) -> MapToken:
        if key in self.store:
            return self.store[key]
        return MapToken.Void

    def __delitem__(self, key: Point):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def num_items(self) -> int:
        return len(self.store)


class IntRobot():
    coder: Intcoder
    paint_map: Dict
    pos: Point
    heading: Heading

    def __init__(self, data, input_buffer=None):
        self.coder = Intcoder(data, input_buffer)
        self.heading = Heading.Up
        self.pos = Point(0, 0)
        self.paint_map = {}

    def send_color(self, token: MapToken):
        self.coder.inbuffer.append(token.value)

    def paint(self, token: MapToken):
        self.paint_map[self.pos] = token

    def token_at(self, pt) -> MapToken:
        if pt in self.paint_map:
            c = self.paint_map[pt]
            return c if c != MapToken.Void else MapToken.Black
        return MapToken.Black

    def turn(self, turn: int):
        inc = turn * 2 - 1
        self.heading = Heading((self.heading.value + inc) % 4)

    def move(self):
        polarities = {
            Heading.Up: Point(0, -1),
            Heading.Down: Point(0, 1),
            Heading.Right: Point(1, 0),
            Heading.Left: Point(-1, 0),
        }
        delta = polarities[self.heading]
        newpos = self.pos + delta
        self.pos = newpos

    def do_step(self):
        pixel = self.token_at(self.pos)
        self.send_color(pixel)
        rt_val = self.coder.run_until_input()
        if rt_val.result == RunResult.Halted:
            return rt_val
        [turn, token] = self.coder.outbuffer.pop(), self.coder.outbuffer.pop()  # LIFO
        self.paint(MapToken(token))
        self.turn(turn)
        self.move()

    def run_until_done(self):
        rt_val = None
        while not rt_val:
            rt_val = self.do_step()


def part1(data):
    start = time.time()
    robot = IntRobot(deepcopy(data))
    robot.run_until_done()
    drawn_coords = [x for x in robot.paint_map if x != MapToken.Void]
    run_counter = len(drawn_coords)
    timestamp(start, f"Part 1: {run_counter}")


def part2(data):
    start = time.time()
    robot = IntRobot(deepcopy(data))
    robot.paint_map[Point(0, 0)] = MapToken.White
    robot.run_until_done()
    drawn_coords = [x for x in robot.paint_map if x != MapToken.Void]
    run_counter = len(drawn_coords)
    timestamp(start, f"Part 2: {run_counter}")


if __name__ == "__main__":
    testdata = readnumbers_csv("day11.csv")[0]
    part1(testdata)
    part2(testdata)

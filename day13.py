import time
from copy import deepcopy
from enum import IntEnum
from typing import DefaultDict, List

from lib.intcoder import Intcoder, ReturnVal, RunResult
from lib.utils import readnumbers_csv, timestamp


class Tile(IntEnum):
    Empty = 0,
    Wall = 1,
    Block = 2,
    Paddle = 3,
    Ball = 4,

    @staticmethod
    def parse(s: str):
        return next((k for k, v in TileType.items() if k == s))


TileType = {
    Tile.Empty: "  ",
    Tile.Wall: "##",
    Tile.Block: "[]",
    Tile.Paddle: "__",
    Tile.Ball: "()",
}


class IntArcadeHelper():
    tilemap: DefaultDict

    def render(self):
        chart = []

        for row in self.tilemap.values():
            line = "".join([TileType[tile.value] for tile in row.values()])
            chart.append(line)

        print("\n".join(chart))


class IntArcade(IntArcadeHelper):
    tilemap: DefaultDict
    coder: Intcoder
    score: int
    ball_xpos: int
    paddle_pos: int

    def __init__(self, code):
        self.coder = Intcoder(code)
        self.tilemap = DefaultDict(dict)
        self.score = 0

    def parsemap(self, data: List[int]):
        pc = 0
        total_size = len(data)
        while pc < total_size:
            (pos_x, pos_y, tile_type) = data[pc:pc+3]
            pc += 3

            if tile_type == Tile.Ball.value:
                self.ball_xpos = pos_x

            elif tile_type == Tile.Paddle.value:
                self.paddle_pos = pos_x

            if pos_x == -1 and pos_y == 0:
                self.score = tile_type
                continue

            # uncomment for render
            self.tilemap[pos_y][pos_x] = Tile.parse(tile_type)

    def get_desired_joystick(self):
        if self.paddle_pos < self.ball_xpos:
            return 1
        elif self.paddle_pos > self.ball_xpos:
            return -1
        return 0

    def run_interactive(self):
        rs: ReturnVal = None
        while not rs or rs.result != RunResult.Halted:
            rs = self.coder.run_until_input()
            self.parsemap(self.coder.outbuffer)
            self.coder.outbuffer = []  # clear buffer

            self.coder.inbuffer.append(self.get_desired_joystick())


def part1(data):
    start = time.time()
    arcade = IntArcade(deepcopy(data))
    arcade.coder.run()
    arcade.render()
    num_block_tiles = arcade.coder.outbuffer.count(Tile.Block.value)
    timestamp(start, f"Part 1: {num_block_tiles}")


def part2(data):
    start = time.time()
    code = deepcopy(data)
    code[0] = 2
    arcade = IntArcade(code)
    arcade.run_interactive()
    timestamp(start, f"Part 2: {arcade.score}")


if __name__ == "__main__":
    testdata = readnumbers_csv("day13.csv")[0]
    part1(testdata)
    part2(testdata)

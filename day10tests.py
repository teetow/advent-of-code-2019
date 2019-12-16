import time
from typing import List

from day10 import Mapper
from lib.gfx import Point
from lib.utils import timestamp


class TestMapper(Mapper):
    def render_chart(self) -> List[str]:
        chart = ["".join(x) for x in self.asteroid_map]
        return chart

    @staticmethod
    def plot(chart: List[List[str]], pt: Point, val) -> List[str]:
        line = list(chart[pt.y])
        line[pt.x] = str(val)
        chart[pt.y] = "".join(line)

    @staticmethod
    def render_targets(chart: List[List[str]], targets: List[Point]) -> List[List[str]]:
        for i, pt in enumerate(targets):
            TestMapper.plot(chart, pt, i+1)
        return chart

    def render_vis_chart(self) -> List[str]:
        chart = self.render_chart()
        vistable = self.get_visibility_table()

        for pt in vistable:
            self.plot(chart, pt, len([x for x in self.sweep(pt)]))

        return chart

    def render_zap_chart(self, limit: int = None) -> List[str]:
        chart = self.render_chart()
        targets = self.zap_sweep(limit)
        return self.render_targets(chart, targets)


def part1_testn1():
    m = TestMapper(["..#", ".##", ".##", ])
    vis_chart = m.render_vis_chart()
    assert vis_chart == ["..3", ".44", ".43"]


def part1_test0():
    start = time.time()
    m = TestMapper([".#..#", ".....", "#####", "....#", "...##", ])
    vis_chart = m.render_vis_chart()
    assert vis_chart == [".7..7", ".....", "67775", "....7", "...87"]
    timestamp(start, f"Test 0 passed.")


def part1_test1():
    start = time.time()
    m = TestMapper(["......#.#.", "#..#.#....", "..#######.", ".#.#.###..", ".#..#.....", "..#....#.#", "#..#....#.", ".##.#..###", "##...#..#.", ".#....####", ])
    assert m.get_best_location() == (Point(5, 8), 33)
    timestamp(start, f"Test 1 passed.")


def part1_test2():
    start = time.time()
    m = TestMapper([
        "#.#...#.#.",
        ".###....#.",
        ".#....#...",
        "##.#.#.#.#",
        "....#.#.#.",
        ".##..###.#",
        "..#...##..",
        "..##....##",
        "......#...",
        ".####.###.",
    ])
    assert m.get_best_location() == (Point(1, 2), 35)
    timestamp(start, f"Test 2 passed.")


def part1_test3():
    start = time.time()
    m = TestMapper([
        ".#..#..###",
        "####.###.#",
        "....###.#.",
        "..###.##.#",
        "##.##.#.#.",
        "....###..#",
        "..#.#..#.#",
        "#..#.#.###",
        ".##...##.#",
        ".....#.#..",
    ])
    assert m.get_best_location() == (Point(6, 3), 41)
    timestamp(start, f"Test 3 passed.")


def part1_test4():
    start = time.time()
    m = TestMapper([
        ".#..##.###...#######",
        "##.############..##.",
        ".#.######.########.#",
        ".###.#######.####.#.",
        "#####.##.#.##.###.##",
        "..#####..#.#########",
        "####################",
        "#.####....###.#.#.##",
        "##.#################",
        "#####.##.###..####..",
        "..######..##.#######",
        "####.##.####...##..#",
        ".#####..#.######.###",
        "##...#.##########...",
        "#.##########.#######",
        ".####.#.###.###.#.##",
        "....##.##.###..#####",
        ".#.#.###########.###",
        "#.#.#.#####.####.###",
        "###.##.####.##.#..##",
    ])
    assert m.get_best_location() == (Point(11, 13), 210)
    timestamp(start, f"Test 4 passed.")


def part2_test0():
    m = TestMapper([
        ".#....#####...#..",
        "##...##.#####..##",
        "##...#...#.#####.",
        "..#.....X...###..",
        "..#.#.....#....##",
    ])

    chart1 = m.render_zap_chart(limit=9)
    assert chart1 == [
        ".#....###24...#..",
        "##...##.13#67..9#",
        "##...#...5.8####.",
        "..#.....X...###..",
        "..#.#.....#....##",
    ]

    chart2 = m.render_zap_chart(limit=9)
    assert chart2 == [
        ".#....###.....#..",
        "##...##...#.....#",
        "##...#......1234.",
        "..#.....X...5##..",
        "..#.9.....8....76",
    ]

    chart3 = m.render_zap_chart(limit=9)
    assert chart3 == [
        ".8....###.....#..",
        "56...9#...#.....#",
        "34...7...........",
        "..2.....X....##..",
        "..1..............",
    ]

    killsheet = m.zap_EVERYTHING()
    final = TestMapper.render_targets(m.render_chart(), killsheet)
    assert final == [
        "......234.....6..",
        "......1...5.....7",
        ".................",
        "........X....89..",
        ".................",
    ]


def test():
    # Part 1 tests
    part1_testn1()
    part1_test0()
    part1_test1()
    part1_test2()
    part1_test3()
    part1_test4()
    print("Part 1 tests passed.")

    # Part 2 tests
    part2_test0()
    print("Part 2 tests passed.")


test()

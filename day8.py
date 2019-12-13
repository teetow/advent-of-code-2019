import time
from dataclasses import dataclass
from typing import List, NamedTuple

from lib.gfx import Point
from lib.utils import timestamp




@dataclass
class Layer:
    chunks: List[str]

    def __init__(self, data: List[str] = None, size: Point = None):
        self.chunks = []

        if data:
            for chunk in data:
                self.chunks.append(chunk)

        if size:
            self.chunks = [" "*size.x for y in range(size.y)]

    def __repr__(self):
        return str([x for x in self.chunks])

    @property
    def num_zeros(self) -> int:
        num_zeros = 0
        for chunk in self.chunks:
            num_zeros += chunk.count("0")
        return num_zeros

    def getpixel(self, point: Point) -> str:
        return self.chunks[point.y][point.x]

    def putpixel(self, point: Point, value: int):
        row = list(self.chunks[point.y])
        row[point.x] = value
        self.chunks[point.y] = "".join(row)


class Sif:
    layers: List[Layer]
    size: Point

    def __init__(self, size: Point):
        self.layers = []
        self.size = size

    def __repr__(self):
        return str([x for x in self.layers])

    @property
    def chunksize(self):
        return self.size.x * self.size.y

    def loadLayer(self, data: List[str]):
        layer = Layer(data)
        self.layers.append(layer)

    def get_merged_layers(self) -> Layer:
        img = Layer(size=self.size)
        layer: Layer
        for layer in reversed(self.layers):
            for y in range(self.size.y):
                for x in range(self.size.x):
                    pt = Point(x, y)
                    src = layer.getpixel(pt)
                    if src != "2":
                        img.putpixel(pt, src)
        return img

    def pretty_render(self) -> str:
        def pretty_pixel(val: str):
            return ["∙∙", "OO", "  "][int(val)]

        img = self.get_merged_layers()
        outstr = ""
        for chunk in img.chunks:
            pretty_row = "".join([pretty_pixel(x) for x in chunk])
            outstr += f"[{pretty_row}]\n"
        return outstr


def parse_sif(data: str, size: Point):
    sif = Sif(size)
    data_chunks = [data[i:i+size.x] for i in range(0, len(data), size.x)]
    data_layers = [data_chunks[i: i+size.y] for i in range(0, len(data_chunks), size.y)]
    for layerdata in data_layers:
        sif.loadLayer(layerdata)
    return sif


def load_sif(fn: str):
    with open(fn, "r") as infile:
        return infile.read()


def test():
    # Part 1 tests
    sif0 = parse_sif("123456789012", Point(3, 2))
    assert sif0.__repr__() == "[['123', '456'], ['789', '012']]"

    t0zeroes = [layer.num_zeros for layer in sif0.layers]
    assert t0zeroes[0] == 0
    assert t0zeroes[1] == 1
    print("Part 1 tests passed.")

    # Part 2 tests
    sif1 = parse_sif("0222112222120000", Point(2, 2))
    sif1result = sif1.get_merged_layers().chunks
    assert sif1result == ["01", "10"]
    print("Part 2 tests passed.")


test()


def part1(sif_data: str):
    start = time.time()
    sif = parse_sif(sif_data, Point(25, 6))
    zero_count = [{"index": i, "zeros": layer.num_zeros} for i, layer in enumerate(sif.layers)]
    best_layer = sif.layers[min(zero_count, key=lambda x: x["zeros"])["index"]]
    num_ones = sum([chunk.count("1") for chunk in best_layer.chunks])
    num_twos = sum([chunk.count("2") for chunk in best_layer.chunks])
    checksum = num_ones * num_twos
    timestamp(start, f"Part 1: {checksum}")


def part2(sif_data):
    start = time.time()
    sif = parse_sif(sif_data, Point(25, 6))
    render = sif.pretty_render()
    timestamp(start, f"Part 2\nPart 2 result: \n{render}")


testdata = load_sif("day8.sif")

part1(testdata)
part2(testdata)

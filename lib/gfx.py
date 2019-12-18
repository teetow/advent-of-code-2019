import math as m
from copy import deepcopy
from dataclasses import dataclass
from typing import Callable, Dict, List


@dataclass(frozen=True)
class Point():
    x: int = 0
    y: int = 0

    def __add__(self, other: "Point"):
        return Point(self.x + other.x, self.y + other.y)


QUADS = {
    (1, -1): 1,
    (1, 1): 2,
    (-1, 1): 3,
    (-1, -1): 4,
}


class FracCoord():
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = x

        if not x == y == 0:
            d = m.gcd(abs(x), abs(y))
            self.x = x // d
            self.y = y // d

    def __repr__(self):
        return f"FC({self.x}, {self.y})"

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other: "FracCoord"):
        return self.x == other.x and self.y == other.y

    @staticmethod
    def get_quadrant(p: Point) -> int:
        if p.x == 0:
            return 3 if p.y >= 0 else 1
        if p.y == 0:
            return 2 if p.x >= 0 else 4

        polarity = (p.x // abs(p.x), p.y // abs(p.y))

        return QUADS[polarity]

    def __lt__(self, other: "FracCoord"):
        q_self = FracCoord.get_quadrant(self)
        q_other = FracCoord.get_quadrant(other)

        if q_self == q_other:
            return (self.x * -other.y) < (-self.y * other.x)

        return q_self < q_other

    def __le__(self, other: "FracCoord"):
        if self.x == other.x and self.y == other.y:
            return True
        return self.__lt__(other)


class MapRender():
    """
    Render a dict of Points and any kind of value to a list of strings.
    Optionally uses a callback to resolve the map symbol to plot.
    """
    token_resolver: Callable[[any], str]

    def __init__(self, token_resolver: Callable[[any], str] = None):
        self.token_resolver = token_resolver if token_resolver else None

    def render(self, data: Dict[Point, any], token_resolver: Callable[[any], str] = None) -> List[str]:
        if token_resolver:
            self.token_resolver = token_resolver
        paint_map = deepcopy(data)
        keys = paint_map.keys()
        xvals = [coord.x for coord in keys]
        xmin = min(xvals)-1
        xmax = max(xvals)+1
        width = max(5, (xmax - xmin)*2)

        yvals = [coord.y for coord in keys]
        ymin = min(yvals)-1
        ymax = max(yvals)+1
        height = max(5, (ymax - ymin)*2)
        fill_char = self.token_resolver(0) if self.token_resolver else "."
        chart = [fill_char * (width) for y in range(height)]

        def plot(pt: Point, val):
            line = chart[pt.y]
            chars = list(line)
            chars[pt.x] = val
            chart[pt.y] = "".join(chars)

        offset = Point(width // 2, height // 2)
        for pt, token in paint_map.items():
            token_char = token_resolver(token) if self.token_resolver else "#"
            plot(pt + offset, token_char)

        return chart


def test():
    pass


if __name__ == "__main__":
    test()

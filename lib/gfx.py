import math as m
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


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

def test():
    pass


if __name__ == "__main__":
    test()

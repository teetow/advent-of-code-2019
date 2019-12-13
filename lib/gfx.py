import math as m
from functools import lru_cache
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Polar(NamedTuple):
    r: float
    theta: float

    @staticmethod
    @lru_cache
    def from_rect(dx, dy) -> "Polar":
        return Polar(calc_r(dx, dy), calc_theta(dx, dy))


def calc_r(dx, dy):
    return m.sqrt(dx*dx + dy*dy)


def calc_theta(dx, dy):
    if dx == 0:
        theta = m.pi / 2 if dy >= 0 else -m.pi / 2
    else:
        theta = m.atan2(dy, dx)
    return theta

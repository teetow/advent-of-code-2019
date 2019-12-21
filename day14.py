import math as m
import time
from collections import Counter
from dataclasses import dataclass
from typing import List

from lib.utils import readdata, timestamp


@dataclass
class Yield:
    quantity: int
    element_name: str

    def __init__(self, quantity: int = 0, element_name: str = ""):
        self.quantity = quantity
        self.element_name = element_name
        super().__init__()


class Reaction(Yield):
    sources: List[Yield]

    def __init__(self):
        super().__init__()
        self.sources: List[Yield] = []
        self.quantity = 0
        self.element_name = ""

    @classmethod
    def from_str(cls, line: str) -> "Reaction":
        r = cls()

        [sources, element] = line.split("=>")
        [qty, element_name] = element.strip().split(" ")
        r.quantity = int(qty)
        r.element_name = element_name

        for source in sources.split(", "):
            [src_qty, src_name] = source.strip().split(" ")
            r.sources.append(Yield(int(src_qty), src_name))
        return r


class Lab:
    inventory: Counter
    reactions: List[Reaction]

    def __init__(self, reaction_data: List[str], initial_stock: Counter = None):
        super().__init__()
        self.reactions: List[Reaction] = []
        self.inventory = Counter()
        if initial_stock:
            self.inventory += initial_stock
        self.parse_data(reaction_data)

    def parse_data(self, reaction_data: List[str]):
        for line in reaction_data:
            self.reactions.append(Reaction.from_str(line))

    def get_reaction(self, element_name: str) -> Reaction:
        return next((x for x in self.reactions if x.element_name == element_name), None)

    def splice_to(self, element_name: str):
        while True:
            success = False
            for el in [x for x in self.inventory if self.inventory[x] > 0 and x != element_name]:
                r = self.get_reaction(el)
                result = self.splice(r)
                if result:
                    success = True
            if not success:
                break

    def splice(self, reaction: Reaction) -> bool:
        el = reaction.element_name
        units_made = m.ceil(self.inventory[el] / reaction.quantity)
        units_used = units_made * reaction.quantity

        if units_used >= reaction.quantity:
            self.inventory[el] -= units_used
            for compound in reaction.sources:
                self.inventory[compound.element_name] += compound.quantity * units_made

            return True

    def calc_max_yield(self, element_name: str, quantity: int):
        # baseline guess
        self.inventory[element_name] = 1
        self.splice_to("ORE")
        fuel_amount = quantity / self.inventory["ORE"]

        while True:
            self.inventory = Counter()
            self.inventory[element_name] = fuel_amount
            self.splice_to("ORE")
            diff = quantity / self.inventory["ORE"]
            # are we getting anywhere?
            if fuel_amount == int(fuel_amount * diff):
                return m.ceil(fuel_amount)
            fuel_amount = int(fuel_amount * diff)


def part1(data):
    start = time.time()
    lab = Lab(data)
    lab.inventory["FUEL"] = 1
    lab.splice_to("ORE")
    ore_spent = lab.inventory["ORE"]
    timestamp(start, f"Part 1: {ore_spent}")


def part2(data):
    start = time.time()
    lab = Lab(data)
    fuel_qty = lab.calc_max_yield("FUEL", 1e12)
    timestamp(start, f"Part 2: {fuel_qty}")


if __name__ == "__main__":
    testdata = readdata("day14.txt")
    part1(testdata)
    part2(testdata)

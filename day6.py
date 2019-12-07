import time
from typing import List

from lib.utils import readdata, timestamp


class Body:
    name: str
    children: List["Body"]
    parent: "Body"

    def __init__(self, name: str):
        self.name = name
        self.children = []
        self.parent = None

    def __repr__(self):
        outstr = ""
        if self.parent:
            outstr += f"{self.parent.name}"
        outstr += f"({self.name})"
        if self.children:
            outstr += ', '.join([x.name for x in self.children])
        return outstr

    def add_child(self, body: "Body"):
        self.children.append(body)

    @property
    def is_root(self):
        return self.parent is None


class Starsystem():
    bodies: List[Body]

    def __init__(self, data: List[str]):
        self.bodies: List[Body] = []
        for entry in data:
            [parent_name, child_name] = entry.split(")")
            p = next((x for x in self.bodies if x.name == parent_name), None)
            if not p:
                p = Body(parent_name)
                self.bodies.append(p)

            c = next((x for x in self.bodies if x.name == child_name), None)
            if not c:
                c = Body(child_name)
                self.bodies.append(c)
            p.children.append(c)
            c.parent = p

    def count_orbits(self) -> int:
        roots = [x for x in self.bodies if x.is_root]
        depth = 0

        def count_links(body_name: str) -> int:
            nonlocal depth
            body = next((x for x in self.bodies if x.name == body_name), None)
            num_links = 0
            depth += 1
            for c in body.children:
                num_links += count_links(c.name) + depth
            depth -= 1
            return num_links

        return count_links(roots[0].name)  # assume one root

    def path_between(self, source_name: str, dest_name: str) -> List[Body]:
        path: List[Body] = []
        target = next((x for x in self.bodies if x.name == source_name), None)
        while target and target.name != dest_name:
            path.append(target)
            target = target.parent

        return path[1:]

    def count_transfers(self, source_name: str, dest_name: str) -> int:
        root = next((x for x in self.bodies if x.is_root), None)
        srcbranch = self.path_between(source_name, root.name)
        destbranch = self.path_between(dest_name, root.name)
        junction = next((s for s in srcbranch if s in destbranch), None)
        transfer_path = srcbranch[0:srcbranch.index(junction)]
        transfer_path += [junction]
        transfer_path += list(reversed(destbranch[0:destbranch.index(junction)]))
        return len(transfer_path) - 1 # two bodies make a jump


def test():
    # Part 1 tests
    t0 = ["COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K", "K)L"]
    s = Starsystem(t0)
    orbits = s.count_orbits()
    assert orbits == 42
    print("Part 1 tests passed.")

    # Part 2 tests
    t1 = ["COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K", "K)L", "K)YOU", "I)SAN"]
    s = Starsystem(t1)
    transfers = s.count_transfers("YOU", "SAN")
    assert transfers == 4
    print("Part 2 tests passed.")


test()


def part1(data):
    start = time.time()
    s = Starsystem(data)
    count = s.count_orbits()
    timestamp(start, f"Part 1: {count}")


def part2(data):
    start = time.time()
    s = Starsystem(data)
    transfers = s.count_transfers("YOU", "SAN")
    timestamp(start, f"Part 2: {transfers}")


testdata = readdata("day6.csv")
part1(testdata)
part2(testdata)

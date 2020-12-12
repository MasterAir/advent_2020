from __future__ import annotations
from typing import NamedTuple, List, Tuple

## Code
dirs = [(1, 0), (0, -1), (-1, 0), (0, 1)]
rot = [((1, 0), (0, 1)), ((0, 1), (-1, 0)), ((-1, 0), (0, -1)), ((0, -1), (1, 0))]


class Ship:
    x: int
    y: int
    dx: int
    dy: int
    f: 0

    def __init__(self):
        self.x = 0
        self.y = 0
        self.f = 0
        self.wx, self.wy = (10, 1)
        self.dx, self.dy = dirs[self.f]

    def follow_instruction(self, inst) -> None:
        inst = inst.strip()
        if inst:
            arg = inst[0]
            val = int(inst[1:])
        else:
            return
        if arg == "N":
            self.y += val
        elif arg == "S":
            self.y -= val
        elif arg == "E":
            self.x += val
        elif arg == "W":
            self.x -= val
        elif arg == "F":
            self.x += val * self.dx
            self.y += val * self.dy
        elif arg == "B":
            self.x += val * self.dx
            self.y += val * self.dy
        elif arg == "L":
            self.f = (self.f - (val // 90)) % 4
            self.dx, self.dy = dirs[self.f]
        elif arg == "R":
            self.f = (self.f + (val // 90)) % 4
            self.dx, self.dy = dirs[self.f]

    def follow_inst2(self, inst: str) -> None:
        inst = inst.strip()
        if inst:
            arg = inst[0]
            val = int(inst[1:])
        else:
            return
        if arg == "N":
            self.wy += val
        elif arg == "S":
            self.wy -= val
        elif arg == "E":
            self.wx += val
        elif arg == "W":
            self.wx -= val
        elif arg == "F":
            self.x += val * self.wx
            self.y += val * self.wy
        elif arg == "B":
            self.x += val * self.wx
            self.y += val * self.wy
        elif arg == "L":
            r = rot[(-val // 90) % 4]
            wx, wy = self.wx, self.wy
            self.wx = wx * r[0][0] + wy * r[0][1]
            self.wy = wx * r[1][0] + wy * r[1][1]
            print(r)
        elif arg == "R":
            r = rot[(val // 90) % 4]
            wx, wy = self.wx, self.wy
            self.wx = wx * r[0][0] + wy * r[0][1]
            self.wy = wx * r[1][0] + wy * r[1][1]

    def man_dist(self, x=0, y=0):
        return abs(self.x - x) + abs(self.y - y)


## Unit Tests
RAW = """F10
N3
F7
R90
F11"""

s1 = Ship()
for inst in RAW.split("\n"):
    s1.follow_instruction(inst)
print(s1.man_dist())

s1 = Ship()
for inst in RAW.split("\n"):
    s1.follow_inst2(inst)
    print(s1.x, s1.y, s1.wx, s1.wy)

assert s1.man_dist() == 286

## Problem
with open("../inputs/day12.txt") as f:
    raw = f.read()

ferry = Ship()
for inst in raw.split("\n"):
    ferry.follow_instruction(inst)

ferry = Ship()
for inst in raw.split("\n"):
    ferry.follow_inst2(inst)

print(ferry.man_dist())
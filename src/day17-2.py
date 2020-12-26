from __future__ import annotations

from typing import NamedTuple, Set


class ActiveCube(NamedTuple):
    x: int
    y: int
    z: int
    w: int


class Problem(NamedTuple):
    turn: int
    space: Set[ActiveCube]

    def step(self) -> Problem:
        xmin = min(cube.x for cube in self.space) - 1
        xmax = max(cube.x for cube in self.space) + 1
        ymin = min(cube.y for cube in self.space) - 1
        ymax = max(cube.y for cube in self.space) + 1
        zmin = min(cube.z for cube in self.space) - 1
        zmax = max(cube.z for cube in self.space) + 1
        wmin = min(cube.w for cube in self.space) - 1
        wmax = max(cube.w for cube in self.space) + 1

        space = set()
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                for z in range(zmin, zmax + 1):
                    for w in range(wmin, wmax + 1):
                        if (x, y, z, w) in self.space and 2 <= self.neighbours(
                            x, y, z, w
                        ) <= 3:
                            space.add(ActiveCube(x, y, z, w))
                        elif (x, y, z, w) not in self.space and self.neighbours(
                            x, y, z, w
                        ) == 3:
                            space.add(ActiveCube(x, y, z, w))

        return Problem(self.turn + 1, space)

    def neighbours(self, x, y, z, w):
        total = 0
        for xx in range(x - 1, x + 2):
            for yy in range(y - 1, y + 2):
                for zz in range(z - 1, z + 2):
                    for ww in range(w - 1, w + 2):
                        if xx == x and yy == y and zz == z and ww == w:
                            continue
                            # don't count yourself
                        if (xx, yy, zz, ww) in self.space:
                            total += 1
        return total

    def print_zw(self, z, w):
        xmin = min(cube.x for cube in self.space)
        xmax = max(cube.x for cube in self.space)
        ymin = min(cube.y for cube in self.space)
        ymax = max(cube.y for cube in self.space)
        print(f"z = {z}, w = {w}")
        for y in range(ymin, ymax + 1):
            line = ""
            for x in range(xmin, xmax + 1):
                if (x, y, z, w) in self.space:
                    line += "#"
                else:
                    line += "."
            print(line)

    @staticmethod
    def parse(raw: str) -> Problem:
        space = set()
        for y, line in enumerate(raw.split("\n")):
            print
            for x, c in enumerate(line.strip()):
                if c == "#":
                    z = 0
                    w = 0
                    space.add(ActiveCube(x, y, z, w))
        return Problem(turn=0, space=space)


## Unit Test

RAW = """.#.
..#
###
"""

prob = Problem.parse(RAW)
prob_hist = [prob]
for _ in range(6):
    prob_hist.append(prob_hist[-1].step())
assert prob_hist[-1].turn == 6
assert len(prob_hist[-1].space) == 848


## Problem
raw = """.#.#.#..
..#....#
#####..#
#####..#
#####..#
###..#.#
#..##.##
#.#.####
"""

problem = Problem.parse(raw)
problem_hist = [problem]
for _ in range(6):
    problem_hist.append(problem_hist[-1].step())
print(problem_hist[-1])
print(len(problem_hist[-1].space))

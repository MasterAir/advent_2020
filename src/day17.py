from __future__ import annotations

from typing import NamedTuple, Set


class ActiveCube(NamedTuple):
    x: int
    y: int
    z: int


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

        space = set()
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                for z in range(zmin, zmax + 1):
                    if (x, y, z) in self.space and 2 <= self.neighbours(x, y, z) <= 3:
                        space.add(ActiveCube(x, y, z))
                    elif (x, y, z) not in self.space and self.neighbours(x, y, z) == 3:
                        space.add(ActiveCube(x, y, z))

        return Problem(self.turn + 1, space)

    def neighbours(self, x, y, z):
        total = 0
        for xx in range(x - 1, x + 2):
            for yy in range(y - 1, y + 2):
                for zz in range(z - 1, z + 2):
                    if xx == x and yy == y and zz == z:
                        continue
                        # don't count yourself
                    if (xx, yy, zz) in self.space:
                        total += 1
        return total

    def print_z(self, z):
        xmin = min(cube.x for cube in self.space)
        xmax = max(cube.x for cube in self.space)
        ymin = min(cube.y for cube in self.space)
        ymax = max(cube.y for cube in self.space)
        print(f"z = {z}")
        for y in range(ymin, ymax + 1):
            line = ""
            for x in range(xmin, xmax + 1):
                if (x, y, z) in self.space:
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
                    space.add(ActiveCube(x, y, z))
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
assert len(prob_hist[-1].space) == 112


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

from typing import List, Tuple
from math import prod

example_plan = [
    "..##.......",
    "#...#...#..",
    ".#....#..#.",
    "..#.#...#.#",
    ".#...##..#.",
    "..#.##.....",
    ".#.#.#....#",
    ".#........#",
    "#.##...#...",
    "#...##....#",
    ".#..#...#.#",
]


def count_trees_hit(plan: List[str], dir: Tuple[int, int]) -> int:
    """
    If we pass the plan in direction dir (right, down), how many trees do we pass

    Parameters
    ----------
    plan : List[str]
        plan, open spaces are "." trees are "#"
    dir : Tuple[int, int]
        direction in coordinates right, down

    Returns
    -------
    int
        number of trees hit
    """

    trees = 0
    pos = [0, 0]
    width = len(plan[0])
    while pos[1] < len(plan):
        try:
            if plan[pos[1]][pos[0]] == "#":
                trees += 1
        except:
            breakpoint()
        pos = [p + d for p, d in zip(pos, dir)]
        if pos[0] >= width:
            pos[0] -= width
    return trees


with open("../inputs/day03.txt") as f:
    plan = [line.strip() for line in f.readlines()]

print(count_trees_hit(plan, (3, 1)))

directions = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]

trees = [count_trees_hit(plan, direc) for direc in directions]
print(trees)
print(prod(trees))
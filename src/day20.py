from __future__ import annotations
from typing import NamedTuple, Tuple, List, Set
from collections import Counter


Edge = Tuple[bool, ...]


class Move(NamedTuple):
    dx: int
    dy: int


class Point(NamedTuple):
    x: int
    y: int

    def move(self, m: Move) -> Point:
        return Point(self.x + m.dx, self.y + m.dy)


class Puzzle:
    all_tiles: Set[Tile]
    locs: Dict[Point, int]
    puzzle: Dict[int, Tile]
    seed_tile: int

    def __init__(self, raw):
        all_tiles = set()
        for inp in raw.split("\n\n"):
            tile = Tile.parse(inp)
            if len(all_tiles) == 0:
                all_tiles.add(tile)
                seed_tile = tile.tile_id
            else:
                all_tiles.update(tile.gen_all_tiles())
        self.all_tiles = all_tiles
        self.order = []
        self.seed_tile = seed_tile

    def solve(self):
        locs: Dict[int, Point] = {}

        locs[self.seed_tile] = Point(0, 0)
        puzzle = {t.tile_id: t for t in self.all_tiles if t.tile_id == self.seed_tile}
        remaining = {t for t in self.all_tiles if t.tile_id != self.seed_tile}
        while remaining:
            current_locs = locs.copy()
            for t in current_locs:
                loc = locs[t]
                tile = puzzle[t]
                for trial in remaining:
                    move = tile.tile_matches(trial)
                    if move != Move(0, 0):
                        puzzle[trial.tile_id] = trial
                        remaining = {t for t in remaining if t.tile_id != trial.tile_id}
                        locs[trial.tile_id] = loc.move(move)

        self.puzzle = puzzle
        self.locs = {point: tile_id for tile_id, point in locs.items()}

        return locs

    def print_solution(self):
        tilesize = 10
        xmin = min(t.x for t in self.locs)
        xmax = max(t.x for t in self.locs)
        ymin = min(t.y for t in self.locs)
        ymax = max(t.y for t in self.locs)
        outlines = []
        for y in range(ymin, ymax + 1):
            for i in range(1, tilesize - 1):
                to_print = ""
                for x in range(xmin, xmax + 1):
                    tile_id = self.locs[Point(x, y)]
                    tile = self.puzzle[tile_id]
                    to_print += tile.contents.splitlines()[i][1:-1]
                outlines.append(to_print)
                print(to_print)
        return outlines


class Tile(NamedTuple):
    tile_id: int
    orientation: int
    top: Edge
    left: Edge
    right: Edge
    bottom: Edge
    contents: str

    def __repr__(self) -> str:
        # out = "".join("#" if c else "." for c in self.top)
        # for i in range(1, 9):
        #     # print the 2nd to 9th characters for (l) and (r)
        #     cl = "#" if self.left[i] else "."
        #     cr = "#" if self.right[i] else "."
        #     out += "\n" + cl + 8 * " " + cr
        # out += "\n"
        # out += "".join("#" if c else "." for c in self.bottom)
        out = self.contents
        return out

    def rotate_right(self) -> Tile:
        top = tuple(b for b in reversed(self.left))
        left = self.bottom
        right = self.top
        bottom = tuple(b for b in reversed(self.right))
        return Tile(
            self.tile_id,
            (self.orientation + 1) % 8,
            top,
            left,
            right,
            bottom,
            rotate_str_right(self.contents),
        )

    def flip(self) -> Tile:
        top = tuple(b for b in reversed(self.top))
        left = self.right
        right = self.left
        bottom = tuple(b for b in reversed(self.bottom))
        return Tile(
            self.tile_id,
            (self.orientation + 1) % 8,
            top,
            left,
            right,
            bottom,
            flip_block(self.contents),
        )

    def gen_all_tiles(self) -> Set[Tile]:
        out = set()
        tile = self.rotate_right()
        for _ in range(4):
            tile = tile.rotate_right()
            out.add(tile)
        tile = tile.flip()
        for _ in range(4):
            tile = tile.rotate_right()
            out.add(tile)
        return out

    def tile_matches(self, t: Tile) -> Move:
        if self.bottom == t.top:
            return Move(0, 1)
        if self.top == t.bottom:
            return Move(0, -1)
        if self.right == t.left:
            return Move(1, 0)
        if self.left == t.right:
            return Move(-1, 0)
        return Move(0, 0)

    @staticmethod
    def parse(raw: str) -> Tile:
        lines = raw.splitlines()
        tile_id = "".join(c for c in lines[0] if c.isnumeric())
        tile_id = int(tile_id)

        top = tuple([True if c == "#" else False for c in lines[1]])
        bottom = tuple([True if c == "#" else False for c in lines[10]])
        left = tuple([True if line[0] == "#" else False for line in lines[1:12]])
        right = tuple([True if line[-1] == "#" else False for line in lines[1:12]])

        contents = "\n".join(lines[1:])
        return Tile(tile_id, 0, top, left, right, bottom, contents)


def rotate_str_right(s: str) -> str:
    lines = s.split("\n")
    out = ""
    for i, _ in enumerate(lines[0]):
        newline = "".join(line[i] for line in reversed(lines)) + "\n"
        out += newline
    return out[:-1]  # dump the last newline character


def flip_block(s: str) -> str:
    out = ""
    lines = s.split("\n")
    for line in lines:
        newline = "".join(c for c in reversed(line)) + "\n"
        out += newline
    return out[:-1]  # dump the last newline character


def find_monster(monster: str, sea: List[str]) -> str:
    # find the dimensions of the monster
    # Monster needs its strings to be the same length
    # and have no trailing or leading whitespace

    monster_mask = [m for m in monster.splitlines() if m.strip()]
    monster_width = len(monster_mask[0])
    monster_height = len(monster_mask)

    sea_width = len(sea[0])
    sea_height = len(sea)
    monsters = []
    for x in range(sea_width - monster_width):
        for y in range(sea_height - monster_height):
            # for y in range(2, 3):
            block = "\n".join(
                [line[x : x + monster_width] for line in sea[y : y + monster_height]]
            )

            if check_block_for_monster(block, monster):
                print(f"monster at ({x}, {y})")
                monsters.append(Point(x, y))

    return monsters


def check_block_for_monster(block: str, monster: str) -> bool:
    assert len(block) == len(monster)
    for i, s, m in zip(range(100), block, monster):
        # print(s, m)
        if m == "#" and s != "#":
            # print("mismatch at character {i}")
            return False
    return True


def rotate_sea(sea: List[str]) -> List[str]:
    joined = "\n".join(sea)
    joined = rotate_str_right(joined)
    return joined.split("\n")


## Unit Tests

RAW = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###"""

MONSTER = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""
MONSTER = MONSTER[1:-1]
t1 = Tile.parse(RAW)
assert t1.tile_id == 2311
assert t1.top == (False, False, True, True, False, True, False, False, True, False)
assert t1.bottom == (False, False, True, True, True, False, False, True, True, True)
assert t1.left == (False, True, True, True, True, True, False, False, True, False)
assert t1.right == (False, False, False, True, False, True, True, False, False, True)

RAW = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""

p_ut = Puzzle(RAW)


## Puzzle
with open("../inputs/day20.txt") as f:
    raw = f.read()

puzzle = Puzzle(raw)
locs = puzzle.solve()
print(locs)

sea = puzzle.print_solution()

backwards_monster = flip_block(MONSTER)

monsters = []
backwards_monsters = []
while not monsters or backwards_monsters:
    sea = rotate_sea(sea)
    monsters = find_monster(MONSTER, sea)
    backwards_monsters = find_monster(backwards_monster, sea)

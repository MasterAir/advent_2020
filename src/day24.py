from __future__ import annotations
from typing import NamedTuple, Dict
from collections import defaultdict


class Dir(NamedTuple):
    dx: int
    dy: int


DIRECTIONS = {
    "e": Dir(2, 0),
    "w": Dir(-2, 0),
    "ne": Dir(1, 1),
    "nw": Dir(-1, 1),
    "se": Dir(1, -1),
    "sw": Dir(-1, -1),
}


class Point(NamedTuple):
    x: int
    y: int

    def move(self, d: Dir) -> Point:
        return Point(self.x + d.dx, self.y + d.dy)

    def find_neighbours(self) -> List[Point]:
        return [self.move(d) for d in DIRECTIONS.values()]


def split_directions(raw: str) -> List[str]:
    out_directions = []
    while raw:
        if raw[0] in DIRECTIONS:
            d, raw = raw[:1], raw[1:]
            out_directions.append(d)
        elif raw[:2] in DIRECTIONS:
            d, raw = raw[:2], raw[2:]
            out_directions.append(d)
        else:
            raise RuntimeError(f"Unexpected direction in {raw}")
    return out_directions


class Grid:
    tiles: Dict[Point, int]

    def __init__(self) -> None:
        self.tiles = defaultdict(lambda: 0)

    def update_tile(self, raw: str) -> None:
        here = Point(0, 0)

        directions = split_directions(raw)
        for direction in directions:
            here = here.move(DIRECTIONS[direction])

        if here in self.tiles:
            self.tiles[here] = (self.tiles[here] + 1) % 2
        else:
            self.tiles[here] = 1

    def update_day(self) -> None:
        black_tiles = {t for t in self.tiles if self.tiles[t] == 1}
        all_neighbours = set()
        for t in black_tiles:
            all_neighbours = all_neighbours.union(t.find_neighbours())
        all_candidates = all_neighbours.union(black_tiles)

        new_tiles = defaultdict(lambda: 0)

        for tile in all_candidates:
            black_neighbours = sum(self.tiles[t] for t in tile.find_neighbours())
            if self.tiles[tile] == 1 and 0 < black_neighbours < 3:
                new_tiles[tile] = 1
            if self.tiles[tile] == 0 and black_neighbours == 2:
                new_tiles[tile] = 1
        self.tiles = new_tiles

        return black_tiles

    ## Unit tests


RAW = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

tiles = Grid()
for line in RAW.splitlines():
    tiles.update_tile(line)

for day in range(101):
    print(f"day {day}: {sum(v for v in tiles.tiles.values())}")
    tiles.update_day()

# assert sum(v for v in tiles.tiles.values()) == 10

## Problem
with open("../inputs/day24.txt") as f:
    raw = f.read()

tiles = Grid()
for line in raw.splitlines():
    tiles.update_tile(line)
print(sum(v for v in tiles.tiles.values()))

for day in range(101):
    print(f"day {day}: {sum(v for v in tiles.tiles.values())}")
    tiles.update_day()
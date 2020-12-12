from __future__ import annotations

from typing import NamedTuple, List, Tuple


class Seat(NamedTuple):
    x: int
    y: int
    occupied: bool

    def is_neighbour(self, s: Seat) -> bool:
        return (
            s.occupied
            and (-1 <= s.x - self.x <= 1)
            and (-1 <= s.y - self.y <= 1)
            and s != self
        )


class Floor:
    seats: List[Seat]
    ys: List[int]
    size: Tuple[int, int]
    steady: bool
    by_xy: dict[Tuple, bool]

    def __init__(self, raw: str) -> None:
        seats = []
        ys = []
        for y, line in enumerate(raw.split("\n")):
            ys.append(len(seats))
            for x, c in enumerate(line.strip()):
                if c == "L":
                    seats.append(Seat(x, y, False))
                elif c == "#":
                    seats.append(Seat(x, y, True))
                elif c == ".":
                    pass
                else:
                    raise RuntimeError(f"Unexpected seat: {c}")
        # seats in the last 2 rows need to look to the end of the grid.
        ys.append(len(seats))
        ys.append(len(seats))

        self.seats = seats
        self.ys = ys
        self.size = (max([s.x for s in seats]), max([s.y for s in seats]))
        self.steady = False
        self.to_byxy()

    def to_byxy(self) -> None:
        self.by_xy = {(s.x, s.y): s.occupied for s in self.seats}

    def __repr__(self):
        seats = set(self.seats)
        fl = ""
        for y in range(self.size[1] + 1):
            line = ""
            for x in range(self.size[0] + 1):
                if Seat(x, y, True) in seats:
                    line += "#"
                elif Seat(x, y, False) in seats:
                    line += "L"
                else:
                    line += "."
            fl += line + "\n"
        return fl

    def timestep(self) -> None:
        n_seats = []
        for seat in self.seats:
            ymin = self.ys[max(0, seat.y - 1)]
            ymax = self.ys[seat.y + 2]
            neighbours = sum([seat.is_neighbour(s) for s in self.seats[ymin:ymax]])
            if neighbours == 0 and not seat.occupied:
                n_seats.append(Seat(seat.x, seat.y, True))
            elif neighbours >= 4 and seat.occupied:
                n_seats.append(Seat(seat.x, seat.y, False))
            else:
                n_seats.append(seat)
        assert len(n_seats) == len(self.seats)

        self.steady = True
        for olds, ns in zip(self.seats, n_seats):
            if olds.x != ns.x:
                raise RuntimeError("reordered seats?")
            if olds.y != ns.y:
                raise RuntimeError("reordered seats?")
            if olds.occupied != ns.occupied:
                self.steady = False
                print()
                print(olds, " -> ", ns)
                print()
                break

        self.seats = n_seats
        self.to_byxy()

    def timestep2(self) -> None:
        n_seats = []
        for seat in self.seats:
            neighbours = self.find_neighbours(seat)
            if neighbours == 0 and not seat.occupied:
                n_seats.append(Seat(seat.x, seat.y, True))
            elif neighbours >= 5 and seat.occupied:
                n_seats.append(Seat(seat.x, seat.y, False))
            else:
                n_seats.append(seat)
        assert len(n_seats) == len(self.seats)

        self.steady = True
        for olds, ns in zip(self.seats, n_seats):
            if olds.x != ns.x:
                raise RuntimeError("reordered seats?")
            if olds.y != ns.y:
                raise RuntimeError("reordered seats?")
            if olds.occupied != ns.occupied:
                self.steady = False
                print()
                print(olds, " -> ", ns)
                print()
                break

        self.seats = n_seats
        self.to_byxy()

    def count_occupied(self) -> int:
        return sum([s.occupied for s in self.seats])

    def in_grid(self, loc: Tuple) -> bool:
        return 0 <= loc[0] <= self.size[0] and 0 <= loc[1] <= self.size[1]

    def find_neighbours(self, s: Seat, adjacent=False) -> int:
        dir = [
            (-1, -1),
            (0, -1),
            (1, -1),
            (-1, 0),
            (1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
        ]
        neighbours = 0
        for dir in dir:
            loc = (s.x + dir[0], s.y + dir[1])
            if adjacent:
                if loc in self.by_xy:
                    neighbours += self.by_xy[loc]
                continue
            while self.in_grid(loc):
                if loc in self.by_xy:
                    neighbours += self.by_xy[loc]
                    break
                else:
                    loc = (loc[0] + dir[0], loc[1] + dir[1])

        return neighbours


## Unit tests
RAW = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""


f1 = Floor(RAW)

while not f1.steady:
    f1.timestep()

assert f1.count_occupied() == 37

R3 = """.............
.L.L.#.#.#.#.
............."""

f3 = Floor(R3)
assert f3.find_neighbours(Seat(1, 1, False)) == 0


R4 = """.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#....."""

f4 = Floor(R4)
seat = [s for s in f4.seats if not s.occupied][0]
assert f4.find_neighbours(seat) == 8

f1 = Floor(RAW)
while not f1.steady:
    f1.timestep2()
    print(f1)
assert f1.count_occupied() == 26


# # puzzle
with open("../inputs/day11.txt") as f:
    raw = f.read()
# fp = Floor(raw)
# while not fp.steady:
#     fp.timestep()
# print(fp.count_occupied())

fp2 = Floor(raw)
while not fp2.steady:
    fp2.timestep2()
print(fp2.count_occupied())

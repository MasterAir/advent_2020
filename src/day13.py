from typing import List, Tuple, NamedTuple, Iterator


class Bus(NamedTuple):
    num: int
    offset: int


def parse_input(raw: str) -> Tuple[int, List[int], List[Bus]]:
    inp = raw.split("\n")
    earliest = int(inp[0])
    buses = [int(i) for i in inp[1].split(",") if i.isnumeric()]
    bus_offset = [
        Bus(int(i), idx % int(i))
        for idx, i in enumerate(inp[1].split(","))
        if i.isnumeric()
    ]
    return (earliest, buses, bus_offset)


def gen_magic_times(bus1: Bus, bus2: Bus) -> Iterator[int]:
    i = 0
    # if bus1 == bus2:
    step = bus1.num
    # else:
    #     step = bus2.num * bus1.num
    while True:
        trial = i * step + bus1.offset
        # print(trial)
        i += 1
        if trial % bus2.num == bus2.offset:
            yield trial


def combine_buses(bus1: Bus, bus2: Bus) -> Bus:
    a1, a2 = [a for _, a in zip(range(2), gen_magic_times(bus1, bus2))]
    offset = a1
    num = a2 - a1
    return Bus(num, offset)


def next_bus(earliest: int, buses: List[int]) -> Tuple[int]:
    my_bus, time = 0, earliest
    for bus in buses:
        time_after_earliest = bus - (earliest % bus)
        print(bus, time_after_earliest)
        if time_after_earliest < time:
            my_bus = bus
            time = time_after_earliest
    return (my_bus, time)


def find_first_magic_time(offset: List[Bus]) -> int:
    megabus = offset[0]
    for bus1 in offset:
        megabus = combine_buses(megabus, bus1)
        print(megabus)
    return megabus.num - megabus.offset


## Unit test


RAW = """939
7,13,x,x,59,x,31,19"""

earliest, buses, bus_offset1 = parse_input(RAW)
my_bus, wait_time = next_bus(earliest, buses)
assert my_bus * wait_time == 295
print(bus_offset1)

megabus = bus_offset1[0]
for bus1 in bus_offset1:
    megabus = combine_buses(megabus, bus1)
print(megabus)

TEST1 = """1
17,x,13,19"""
_, _, offset = parse_input(TEST1)
assert find_first_magic_time(offset) == 3417

TEST2 = """1
67,7,59,61"""
_, _, offset = parse_input(TEST2)
assert find_first_magic_time(offset) == 754018

TEST3 = """1
1789,37,47,1889"""
_, _, offset = parse_input(TEST3)
assert find_first_magic_time(offset) == 1202161486


raw = """1003240
19,x,x,x,x,x,x,x,x,41,x,x,x,37,x,x,x,x,x,787,x,x,x,x,x,x,x,x,x,x,x,x,13,x,x,x,x,x,x,x,x,x,23,x,x,x,x,x,29,x,571,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,17"""

earliest, buses, bus_offset = parse_input(raw)
my_bus, wait_time = next_bus(earliest, buses)
# print(my_bus * wait_time)
print(find_first_magic_time(bus_offset))

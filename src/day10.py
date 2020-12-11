from typing import List


def find_differences(adaptors: List[int]) -> List[int]:
    """
    Given a list of adaptors, order them and return a list
    of differences

    Parameters
    ----------
    adaptors : List[int]
        List of adaptor joltages

    Returns
    -------
    List[int]
        Difference in joltage between the adaptors
    """
    # Add base adaptor and device's adaptor to list
    sa = [0] + sorted(adaptors) + [max(adaptors) + 3]
    return [j - i for i, j in zip(sa, sa[1:])]


def find_combinations(adaptors: List[int]) -> int:
    diffs = find_differences(adaptors)
    # every time there's a 3 both ends are required
    # 1s in a row:
    combs = (1, 1, 2, 4, 7)
    paths = 1
    con_1 = 0
    for x, i in enumerate(diffs):
        if i == 1:
            con_1 += 1
        if i == 3:
            paths *= combs[con_1]
            con_1 = 0
        print(i, paths)
    return paths


def longest_string_of_1(diffs):
    curr_1s = 0
    max_1s = 0
    for i in diffs:
        if i == 1:
            curr_1s += 1
        else:
            max_1s = max(curr_1s, max_1s)
            curr_1s = 0
    return max_1s


def path_ok(adaptor):
    return max(find_differences) <= 3


## Tests

RAW = """16
10
15
5
1
11
7
19
6
12
4"""

RAW2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

ADAPTORS = [int(i) for i in RAW.split("\n")]
diffs = find_differences(ADAPTORS)
print(diffs.count(1), diffs.count(3))

ADAPTORS2 = [int(i) for i in RAW2.split("\n")]
diffs = find_differences(ADAPTORS2)
print(diffs.count(1), diffs.count(3))

assert find_combinations(ADAPTORS) == 8
assert find_combinations(ADAPTORS2) == 19208

### Problem

with open("../inputs/day10.txt") as f:
    adaptors = [int(line) for line in f]
diffs = find_differences(adaptors)
print(diffs.count(1) * diffs.count(3))
print(diffs.count(1), diffs.count(2), diffs.count(3))
print(find_combinations(adaptors))
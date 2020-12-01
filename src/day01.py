from typing import List

with open("../inputs/day01.txt") as f:
    data = [int(i.strip()) for i in f]


def find_2020(data: List[int], val: int = 2020) -> int:
    """
    Returns the product of the 2 values in data that sum to val

    Parameters
    ----------
    data : List[int]
        numbers from which we're looking for a pair that sum to val
    val : int, optional
        value that we're looking for, by default 2020

    Returns
    -------
    int
        product of the 2 numbers that sum to val if they exist and 0 otherwise
    """
    data = set(data)
    for i in data:
        if val - i in data:
            return i * (val - i)
    return 0


def find_2020_3(data: List[int], val: int = 2020) -> int:
    """
    Find the product of 3 values that sum to val (2020)

    Parameters
    ----------
    data : List[int]
        List of ints where we're searching for a triple.
    val : int, optional
        Value we want the triple to sum to, by default 2020

    Returns
    -------
    int
        Product of a triple that sum to val, 0 if such a triple doesn't exist
    """
    for i in data:
        needs = val - i
        a = find_2020(data, needs)
        if a:
            return i * a
    return 0


dummy = [
    1721,
    979,
    366,
    299,
    675,
    1456,
]
assert find_2020(dummy) == 514579
assert find_2020_3(dummy) == 241861950
print(find_2020_3(data))
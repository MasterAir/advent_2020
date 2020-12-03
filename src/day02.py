dummy = """
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
"""


def validate_code(line: str) -> bool:
    """
    Does this line's rules make this line's code valid?
    Rules state the number of times a particular character must appear.

    Parameters
    ----------
    line : str
        line of input containing rules and code

    Returns
    -------
    bool
        is this line valid
    """
    try:
        (rules, code) = line.split(":")
    except:
        return False

    ch = rules[-1]
    min_occ, max_occ = rules.split("-")
    min_occ = int(min_occ)
    max_occ = int(max_occ.split()[0])

    return code.count(ch) >= min_occ and code.count(ch) <= max_occ


def validate_code_2(line: str) -> bool:
    """
    Does this line's rules make this line's code valid?
    Rules are 2 positions it the code, exactly 1 must match the character.
    Positions are 1 based (i.e. 1 is the first position in the code)

    Parameters
    ----------
    line : str
        line of input containing rules and code

    Returns
    -------
    bool
        is this line valid
    """
    try:
        (rules, code) = line.split(":")
        code = code.strip()
    except:
        return False

    ch = rules[-1]
    first, last = rules.split("-")
    first = int(first) - 1
    last = int(last.split()[0]) - 1

    if first == last:
        print("cheeky")
        return code[first] == ch

    # Use != between booleans for xor
    return (code[first] == ch) != (code[last] == ch)


assert sum([validate_code(line) for line in dummy.splitlines()]) == 2
assert sum([validate_code_2(line) for line in dummy.splitlines()]) == 1

with open("../inputs/day02.txt") as f:
    valid = [validate_code_2(line) for line in f]

print(sum(valid))
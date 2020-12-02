dummy = """
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
"""


def validate_code(line: str) -> bool:
    """
    Does this line's rules make this line's code valid?

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


assert sum([validate_code(line) for line in dummy.splitlines()]) == 2

with open("../inputs/day02.txt") as f:
    valid = [validate_code(line) for line in f]

print(sum(valid))
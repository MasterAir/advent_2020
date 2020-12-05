from __future__ import annotations

from typing import NamedTuple

INPUTS = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

fields = [
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
    "cid",
]


class Passport(NamedTuple):
    byr: int = None
    iyr: int = None
    eyr: int = None
    hgt: str = None
    hcl: str = None
    ecl: str = None
    pid: int = None
    cid: int = None

    def is_valid_simple(self) -> bool:
        for i in self[:-1]:
            if i is None:
                return False
        return True

    def is_valid(self) -> bool:
        try:
            if not self.is_valid_simple():
                return False

            if len(self.byr) != 4:
                return False
            if not 1920 <= int(self.byr) <= 2002:
                return False

            if len(self.iyr) != 4:
                return False
            if not 2010 <= int(self.iyr) <= 2020:
                return False

            if len(self.eyr) != 4:
                return False
            if not 2020 <= int(self.eyr) <= 2030:
                return False

            try:
                val, units = int(self.hgt[:-2]), self.hgt[-2:]
            except ValueError:
                ## catch 2 numbers no units
                return False
            if units == "in":
                if not 59 <= val <= 76:
                    return False
            elif units == "cm":
                if not 150 <= val <= 193:
                    return False
            else:
                return False

            if len(self.hcl) != 7:
                return False

            if self.hcl[0] != "#":
                return False
            for c in self.hcl[1:]:
                if not (c.isnumeric() or c in {"a", "b", "c", "d", "e", "f"}):
                    return False

            if self.ecl not in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}:
                return False

            if len(self.pid) != 9 or not self.pid.isnumeric():
                return False

            return True
        except:
            breakpoint()

    @staticmethod
    def parse(inp: str) -> Passport:
        parse_dict = {}
        for field in inp.split():
            place, val = field.split(":")
            parse_dict[place] = val

        return Passport(**parse_dict)


passports = [Passport.parse(inp) for inp in INPUTS.split("\n\n")]
# assert sum([passp.is_valid() for passp in passports]) == 2


with open("../inputs/day04.txt") as f:
    input_data = f.read()

passports = [Passport.parse(inp) for inp in input_data.split("\n\n")]
print(sum([passp.is_valid() for passp in passports]))

invalid_pass = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""

valid_pass = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""

passports = [Passport.parse(inp) for inp in invalid_pass.split("\n\n")]
print([passp.is_valid() for passp in passports])
passports = [Passport.parse(inp) for inp in valid_pass.split("\n\n")]
print([passp.is_valid() for passp in passports])
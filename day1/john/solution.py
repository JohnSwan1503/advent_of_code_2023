import re
from enum import Enum

class Number(Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9

starting_char = set(_[0] for _ in Number.__members__)
digit_chars = set(_ for _ in "".join([c for m in Number.__members__ for c in m]))

with open('input.txt', 'r') as f: # I'm stuck on windows for work so make sure to update for your OS
    
    f_digits = []
    for line in f:
        l_digits = []
        chars: list = []

        for c in line.strip():

            if c.isnumeric():
                l_digits.append(int(c))
                chars = []
                continue

            if not chars and c not in starting_char:
                continue

            if c not in digit_chars:
                chars = []
                continue

            chars.append(c)

            if len(chars) >= 3:
                chars_str = "".join(chars)
                for m in Number.__members__:
                    if m in chars_str:
                        l_digits.append(Number[m].value)
                        chars = chars[-1:]
                        break
                
        f_digits.append((l_digits[0] * 10 + l_digits[-1], line.strip()))

print(f_digits)
print(sum(_[0] for _ in f_digits))

#!/usr/bin/env python3

def load_input(filename):
    instructions = ''
    with open(filename) as f:
        for l in f:
            instructions += l.strip()
    return instructions


def compute_floors(instructions):
    floor = 0
    basement = None
    char = 0
    for c in instructions:
        char += 1
        if c == '(':
            floor += 1
        elif c == ')':
            floor -= 1
        if basement is None and floor < 0:
            basement = char
    return (floor, basement)


instructions = load_input('input.txt')
(floor, basement) = compute_floors(instructions)

print('AOC 2015 01 part 1')
print(floor)

print()

print('AOC 2015 01 part 2')
print(basement)

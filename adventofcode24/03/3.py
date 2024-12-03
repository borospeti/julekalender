#!/usr/bin/env python3

import re


def load_input(filename):
    with open(filename) as f:
        return f.read()


def compute(p):
    s = 0
    for (a, b) in re.findall(r'mul\((\d+),(\d+)\)', p):
        s += int(a) * int(b)
    return s


def compute2(p):
    s = 0
    enabled = True
    for (a, b, do, dont) in re.findall(r'mul\((\d+),(\d+)\)|(do\(\))|(don\'t\(\))', p):
        if do == 'do()':
            enabled = True
            continue
        if dont == 'don\'t()':
            enabled = False
            continue
        if not enabled:
            continue
        s += int(a) * int(b)
    return s


program = load_input('input.txt')

print('AOC 2024 03 part 1')
print(compute(program))

print()

print('AOC 2024 03 part 2')
print(compute2(program))



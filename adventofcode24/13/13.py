#!/usr/bin/env python3

from fractions import Fraction
import re


def load_input(filename):
    machines = []
    with open(filename) as f:
        while line := (f.readline().strip() + ' ' + f.readline().strip() + ' ' + f.readline().strip() + ' ' + f.readline()).strip():
            m = re.match(r'Button A: X\+(\d+), Y\+(\d+) Button B: X\+(\d+), Y\+(\d+) Prize: X=(\d+), Y=(\d+)', line)
            machines.append(list(map(Fraction, m.group(1, 3, 2, 4, 5, 6))))
    return machines


def solve(m, offset):
    (a, b, c, d, x, y) = m
    x += offset
    y += offset
    det = a * d - b * c
    (e, f, g, h) = (d / det, -b / det, -c / det, a / det)
    p = e * x + f * y
    q = g * x + h * y
    if p.is_integer() and q.is_integer():
        return (p, q)
    return None


def calculate_cost(machines, offset=0):
    cost = 0
    for m in machines:
        s = solve(m, offset)
        if s is not None:
            cost += 3 * s[0] + s[1]
    return cost


machines = load_input('input.txt')
#machines = load_input('test.txt')

print('AOC 2024 13 part 1')
print(calculate_cost(machines))

print()

print('AOC 2024 13 part 2')
print(calculate_cost(machines, offset=10000000000000))


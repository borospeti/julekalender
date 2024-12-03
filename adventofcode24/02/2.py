#!/usr/bin/env python3

from math import copysign

def load_input(filename):
    l = []
    with open(filename) as f:
        for line in f:
            l.append([int(x) for x in line.strip().split()])
    return l


def is_safe(m, dampener):
    r = [b - a for (a, b) in zip(m, m[1:])]
    s = copysign(1, r[0])
    ok = all(copysign(1, x) == s and 1 <= abs(x) <= 3 for x in r)
    if ok or not dampener:
        return ok
    for i in range(len(m)):
        if is_safe(m[:i] + m[i+1:], False):
            return True
    return False


def check_safety(l, dampener=False):
    cnt = 0
    for m in l:
        if is_safe(m, dampener):
            cnt += 1
    return cnt


l = load_input('input.txt')

print('AOC 2024 02 part 1')
print(check_safety(l))

print()

print('AOC 2024 02 part 2')
print(check_safety(l, dampener=True))

#!/usr/bin/env python3

from collections import Counter


def load_input(filename):
    l1 = []
    l2 = []

    with open(filename) as f:
        for l in f:
            (a, b) = l.strip().split()
            l1.append(int(a))
            l2.append(int(b))

    return (l1, l2)


def compute_diff(l1, l2):
    s1 = sorted(l1)
    s2 = sorted(l2)
    return sum(abs(p2 - p1) for (p1, p2) in zip(s1, s2))


def compute_sim(l1, l2):
    c2 = Counter(l2)
    return sum(c2[i1] * i1 for i1 in l1)


(l1, l2) = load_input('input.txt')

print('AOC 2024 01 part 1')
print(compute_diff(l1, l2))

print()

print('AOC 2024 01 part 2')
print(compute_sim(l1, l2))

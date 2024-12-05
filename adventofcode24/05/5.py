#!/usr/bin/env python3

def load_input(filename):
    rules = set()
    updates = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue
            if line.find('|') >= 0:
                (a, b) = line.split('|')
                rules.add((int(a), int(b)))
            else:
                updates.append([int(p) for p in line.split(',')])
    return (rules, updates)


def check_update(rules, u):
    for i in range(len(u) - 1):
        for j in range(i + 1, len(u)):
            if (u[j], u[i]) in rules:
                return False
    return True


def sort_pages(rules, u):
    s = [p for p in u]
    for i in range(len(s) - 1):
        swap = True
        while swap:
            swap = False
            for j in range(i + 1, len(s)):
                if (s[j], s[i]) in rules:
                    t = s[j]
                    s[j] = s[i]
                    s[i] = t
                    swap = True
                    break
    return s


def sum_mids(rules, updates):
    good, bad = (0, 0)
    for u in updates:
        if check_update(rules, u):
            good += u[len(u) // 2]
        else:
            v = sort_pages(rules, u)
            bad += v[len(v) // 2]
    return (good, bad)


(rules, updates) = load_input('input.txt')
(good, bad) = sum_mids(rules, updates)

print('AOC 2024 03 part 1')
print(good)

print()

print('AOC 2024 03 part 2')
print(bad)

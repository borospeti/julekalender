#!/usr/bin/env python3

def load_input(filename):
    m = []
    with open(filename) as f:
        for line in f:
            m.append(line.strip())
    return m

def char_at(m, x, y):
    if x < 0 or x >= len(m) or y < 0 or y >= len(m[x]):
        return None
    return m[x][y]


def contains_word(m, w, x, y, dx, dy):
    for c in w:
        if not c == char_at(m, x, y):
            return False
        x += dx
        y += dy
    return True


def count_word_unidir(m, w, x, y):
    count = 0
    for (dx, dy) in [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]:
        if contains_word(m, w, x, y, dx, dy):
            count += 1
    return count


def count_word(m, w):
    count = 0
    for x in range(len(m)):
        for y in range(len(m[x])):
            count += count_word_unidir(m, w, x, y)
    return count


def contains_xmas(m, x, y):
    if char_at(m, x, y) != 'A':
        return False
    ms1 = (char_at(m, x+1, y+1), char_at(m, x-1, y-1))
    if not (ms1 == ('M', 'S') or ms1 == ('S', 'M')):
        return False
    ms2 = (char_at(m, x+1, y-1), char_at(m, x-1, y+1))
    return ms2 == ('M', 'S') or ms2 == ('S', 'M')


def count_xmas(m):
    count = 0
    for x in range(len(m)):
        for y in range(len(m[x])):
            if contains_xmas(m, x, y):
                count += 1
    return count

matrix = load_input('input.txt')

print('AOC 2024 04 part 1')
print(count_word(matrix, 'XMAS'))

print()

print('AOC 2024 04 part 2')
print(count_xmas(matrix))




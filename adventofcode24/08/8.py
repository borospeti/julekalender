#!/usr/bin/env python3

import math


def load_input(filename):
    antennas = {}
    height = 0
    width = 0
    with open(filename) as f:
        for line in f:
            x = height
            y = 0
            for c in line.strip():
                if c != '.':
                    if c not in antennas:
                        antennas[c] = []
                    antennas[c].append((x, y))
                y += 1
            height += 1
            if y > width:
                width = y
    return (antennas, height, width)


def get_antinodes_two(pos1, pos2, height, width):
    a1 = (2 * pos2[0] - pos1[0], 2 * pos2[1] - pos1[1])
    if 0 <= a1[0] < height and 0 <= a1[1] < width:
        yield a1
    a2 = (2 * pos1[0] - pos2[0], 2 * pos1[1] - pos2[1])
    if 0 <= a2[0] < height and 0 <= a2[1] < width:
        yield a2


def get_antinodes_all(pos1, pos2, height, width):
    (dx, dy) = (pos2[0] - pos1[0], pos2[1] - pos1[1])
    g = math.gcd(dx, dy)
    dx = dx // g
    dy = dy // g
    (x, y) = pos1
    while 0 <= x < height and 0 <= y < width:
        yield (x, y)
        x -= dx
        y -= dy
    (x, y) = pos2
    while 0 <= x < height and 0 <= y < width:
        yield (x, y)
        x += dx
        y += dy


def locate_antinodes(antennas, height, width, full_grid=False):
    antinodes = set()
    locator = get_antinodes_all if full_grid else get_antinodes_two
    for positions in antennas.values():
        for i in range(len(positions) - 1):
            for j in range(i + 1, len(positions)):
                antinodes.update(locator(positions[i], positions[j], height, width))
    return antinodes


(antennas, height, width) = load_input('input.txt')

print('AOC 2024 08 part 1')
print(len(locate_antinodes(antennas, height, width)))

print()

print('AOC 2024 08 part 2')
print(len(locate_antinodes(antennas, height, width, full_grid=True)))


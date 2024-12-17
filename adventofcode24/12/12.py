#!/usr/bin/env python3

from collections import deque


def load_input(filename):
    garden = []
    with open(filename) as f:
        for line in f:
            garden.append('.' + line.strip() + '.')
    return ['.' * len(garden[0])] + garden + ['.' * len(garden[0])]


def trace_region(garden, sx, sy, visited):
    if (sx, sy) in visited:
        return None
    region = []
    seed = deque([(sx, sy)])
    rid = garden[sx][sy]
    while len(seed) > 0:
        (x, y) = seed.popleft()
        if (x, y) in visited:
            continue
        region.append((x, y))
        visited.add((x, y))
        for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if (x + dx, y + dy) not in visited and garden[x + dx][y + dy] == rid:
                seed.append((x + dx, y + dy))
    return region


def segment_garden(garden):
    visited = set()
    for x in range(1, len(garden) - 1):
        for y in range(1, len(garden[x]) - 1):
            region = trace_region(garden, x, y, visited)
            if region is not None:
                yield region


def region_edges(garden, region):
    edges = []
    for (x, y) in region:
        for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if garden[x][y] != garden[x + dx][y + dy]:
                edges.append((x, y, dx, dy))
    return edges


def count_sides(edges):
    sides = 0
    for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        filtered = [e for e in edges if e[2] == dx and e[3] == dy]
        if dx == 0:
            filtered = sorted(filtered, key = lambda e: (e[1], e[0]))
            c = 0
            (x, y) = (0, 0)
            for e in filtered:
                if e[0] != x + 1 or e[1] != y:
                    c += 1
                (x, y) = (e[0], e[1])
            sides += c
        else:
            filtered = sorted(filtered, key = lambda e: (e[0], e[1]))
            c = 0
            (x, y) = (0, 0)
            for e in filtered:
                if e[0] != x or e[1] != y + 1:
                    c += 1
                (x, y) = (e[0], e[1])
            sides += c
    return sides


def region_area(garden, region):
    return len(region)


def region_perimeter(garden, region):
    return len(region_edges(garden, region))


def region_sides(garden, region):
    return count_sides(region_edges(garden, region))


def region_price(garden, region, discount=False):
    if discount:
        return region_area(garden, region) * region_sides(garden, region)
    else:
        return region_area(garden, region) * region_perimeter(garden, region)


def calculate_price(garden, discount=False):
    total = 0
    for region in segment_garden(garden):
        total += region_price(garden, region, discount)
    return total


garden = load_input('input.txt')
#garden = load_input('test.txt')
#print(garden)

print('AOC 2024 12 part 1')
print(calculate_price(garden))

print()

print('AOC 2024 12 part 2')
print(calculate_price(garden, discount=True))



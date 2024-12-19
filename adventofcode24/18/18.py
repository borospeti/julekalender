#!/usr/bin/env python3

import re
from heapq import heappush, heappop
from copy import deepcopy


START = 'S'
END = 'E'
WALL = '#'
SPACE = ' '

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

INPUT = 'input.txt'
WIDTH = 71
HEIGHT = 71
INITIAL_BYTES = 1024

#INPUT = 'test.txt'
#WIDTH = 7
#HEIGHT = 7
#INITIAL_BYTES = 12


def load_input(filename):
    hits = []
    with open(filename) as f:
        while line := f.readline().strip():
            hits.append(list(map(int, line.split(','))))
    return hits


def create_field(hits, n):
    field = [[WALL] * (WIDTH + 2)] + [[WALL] + [SPACE] * WIDTH + [WALL] for x in range(HEIGHT)] + [[WALL] * (WIDTH + 2)]
    for i in range(n):
        field[hits[i][0] + 1][hits[i][1] + 1] = WALL
    return field

def print_field(field):
    for l in field:
        print(''.join(l))


def create_nodes(field, graph, x, y):
    edges = []
    for i in range(len(DIRECTIONS)):
        (dx, dy) = DIRECTIONS[i]
        if field[x + dx][y + dy] != WALL:
            edges.append((x + dx, y + dy))
    graph[(x, y)] = edges


def process_field(field):
    graph = {}
    for x in range(len(field)):
        for y in range(len(field[x])):
            if field[x][y] != WALL:
                create_nodes(field, graph, x, y)
    return graph


def find_path(field):
    graph = process_field(field)
    seed = []
    heappush(seed, (0, 1, 1))
    visited = {}
    visited[(1, 1)] = (0, set())
    while len(seed) > 0:
        (cost, x, y) = heappop(seed)
        for (x2, y2) in graph[(x, y)]:
            if (x2, y2) not in visited or cost + 1 < visited[(x2, y2)][0]:
                visited[(x2, y2)] = (cost + 1, set([(x, y)]))
                heappush(seed, (cost + 1, x2, y2))
    if (HEIGHT, WIDTH) in visited:
        return visited[(HEIGHT, WIDTH)][0]
    return None


def find_blocker_byte(field, hits, n):
    left = n
    right = len(hits) - 1
    while right - left > 1:
        pivot = (left + right) // 2
        field2 = deepcopy(field)
        for (x, y) in hits[n:pivot + 1]:
            field2[x + 1][y + 1] = WALL
        if find_path(field2) is None:
            right = pivot
        else:
            left = pivot
    return hits[right]


hits = load_input(INPUT)
field = create_field(hits, INITIAL_BYTES)

#print_field(field)


print('AOC 2024 18 part 1')
print(find_path(field))

print()

print('AOC 2024 18 part 2')
print(','.join(map(str, find_blocker_byte(field, hits, INITIAL_BYTES))))

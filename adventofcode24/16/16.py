#!/usr/bin/env python3

import re
from heapq import heappush, heappop


START = 'S'
END = 'E'
WALL = '#'

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

MOVE_COST = 1
TURN_COST = 1000


def load_input(filename):
    field = []
    with open(filename) as f:
        while line := f.readline().strip():
            field.append(line)
    return field


def print_field(field):
    for l in field:
        print(l)


def create_nodes(field, graph, x, y):
    for i in range(len(DIRECTIONS)):
        (dx, dy) = DIRECTIONS[i]
        edges = []
        if field[x + dx][y + dy] != WALL:
            edges.append((x + dx, y + dy, dx, dy, MOVE_COST))
        edges.append((x, y, DIRECTIONS[(i + 1) % 4][0], DIRECTIONS[(i + 1) % 4][1], TURN_COST))
        edges.append((x, y, DIRECTIONS[(i - 1) % 4][0], DIRECTIONS[(i - 1) % 4][1], TURN_COST))
        graph[(x, y, dx, dy)] = edges


def process_field(field):
    graph = {}
    for x in range(len(field)):
        for y in range(len(field[x])):
            if field[x][y] == START:
                start = (x, y)
            elif field[x][y] == END:
                end = (x, y)
            if field[x][y] != WALL:
                create_nodes(field, graph, x, y)
    return (graph, start, end)

def locate_best_tiles(visited, seed, counted=None):
    if counted is None:
        counted = set()
    if seed in counted:
        return
    counted.add(seed)
    yield seed
    for prev in visited[seed][1]:
        yield from locate_best_tiles(visited, prev, counted)


def find_path(field):
    (graph, start, end) = process_field(field)
    seed = []
    heappush(seed, (0, start[0], start[1], 0, 1))
    visited = {}
    visited[(start[0], start[1], 0, 1)] = (0, set())
    while len(seed) > 0:
        (cost, x, y, dx, dy) = heappop(seed)
        for (x2, y2, dx1, dy2, cost2) in graph[(x, y, dx, dy)]:
            if (x2, y2, dx1, dy2) not in visited or cost + cost2 < visited[(x2, y2, dx1, dy2)][0]:
                visited[(x2, y2, dx1, dy2)] = (cost + cost2, set([(x, y, dx, dy)]))
                heappush(seed, (cost + cost2, x2, y2, dx1, dy2))
            elif cost + cost2 == visited[(x2, y2, dx1, dy2)][0]:
                visited[(x2, y2, dx1, dy2)][1].add((x, y, dx, dy))
                heappush(seed, (cost + cost2, x2, y2, dx1, dy2))
    best = None
    for (dx, dy) in DIRECTIONS:
        cost = visited[(end[0], end[1], dx, dy)][0]
        if best is None or best[1] > cost:
            best = ((end[0], end[1], dx, dy), cost)
    tiles = len(set((x, y) for (x, y, dx, dy) in locate_best_tiles(visited, best[0])))
    return (best[1], tiles)


#field = load_input('input.txt')
field = load_input('test.txt')

#print_field(field)
(cost, tiles) = find_path(field)


print('AOC 2024 16 part 1')
print(cost)

print()

print('AOC 2024 16 part 2')
print(tiles)



#!/usr/bin/env python3

from heapq import heappush, heappop
from collections import Counter


START = 'S'
END = 'E'
WALL = '#'
SPACE = '.'

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def load_input(filename):
    field = []
    with open(filename) as f:
        while line := f.readline().strip():
            field.append(line)
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
            if field[x][y] == START:
                start = (x, y)
            elif field[x][y] == END:
                end = (x, y)
            if field[x][y] != WALL:
                create_nodes(field, graph, x, y)
    return (graph, start, end)


def find_path(graph, start, end):
    seed = []
    heappush(seed, (0, start[0], start[1]))
    visited = {}
    visited[start] = (0, set())
    while len(seed) > 0:
        (cost, x, y) = heappop(seed)
        for (x2, y2) in graph[(x, y)]:
            if (x2, y2) not in visited or cost + 1 < visited[(x2, y2)][0]:
                visited[(x2, y2)] = (cost + 1, set([(x, y)]))
                heappush(seed, (cost + 1, x2, y2))
    return visited


def find_cheats(field, threshold=100, time_limit=2):
    (graph, start, end) = process_field(field)
    forward = find_path(graph, start, end)
    backward = find_path(graph, end, start)
    best = forward[end][0]

    for (x, y) in forward:
        for dx in range(0, time_limit + 1):
            for dy in range(0, time_limit + 1 - dx):
                if (x+dx, y+dy) in backward and (score := forward[(x, y)][0] + backward[(x+dx, y+dy)][0] + dx + dy) <= best - threshold:
                    yield (x, y, x+dx, y+dy, best - score)
                if dy > 0 and (x+dx, y-dy) in backward and (score := forward[(x, y)][0] + backward[(x+dx, y-dy)][0] + dx + dy) <= best - threshold:
                    yield (x, y, x+dx, y-dy, best - score)
                if dx > 0 and (x-dx, y+dy) in backward and (score := forward[(x, y)][0] + backward[(x-dx, y+dy)][0] + dx + dy) <= best - threshold:
                    yield (x, y, x-dx, y+dy, best - score)
                if dx > 0 and dy > 0 and (x-dx, y-dy) in backward and (score := forward[(x, y)][0] + backward[(x-dx, y-dy)][0] + dx + dy) <= best - threshold:
                    yield (x, y, x-dx, y-dy, best - score)


field = load_input('input.txt')
#field = load_input('test.txt')

#for cheat in find_cheats(field, threshold=20, time_limit=2):
#    print(cheat)

print('AOC 2024 18 part 1')
print(sum(1 for cheat in find_cheats(field)))

print()

print('AOC 2024 18 part 2')
print(sum(1 for cheat in find_cheats(field, time_limit=20)))


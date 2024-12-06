#!/usr/bin/env python3

def load_input(filename):
    m = []
    with open(filename) as f:
        for line in f:
            m.append(list(line.strip()))
    return m


def find_guard(m):
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == '^':
                return (i, j)
    return None


def move(m, x, y, dx, dy):
    """returns: (r, x, y, dx, dy)  r is -1: out of map, 0: turn, 1: move"""
    if x + dx < 0 or x + dx >= len(m) or y + dy < 0 or y + dy >= len(m[x + dx]):
        return (-1, 0, 0, 0, 0)
    if m[x + dx][y + dy] == '#':
        return (0, x, y, dy, -dx)
    return (1, x + dx, y + dy, dx, dy)


def walk(m, x, y, dx, dy):
    """returns: the count of visisted cells, or -1 if there is a loop"""
    visited = set()
    while True:
        if (x, y, dx, dy) in visited:
            return -1
        visited.add((x, y, dx, dy))
        (r, x, y, dx, dy) = move(m, x, y, dx, dy)
        if r < 0:
            break
    return len(set((x, y) for (x, y, dx, dy) in visited))


def check_blockers(m, x, y, dx, dy):
    (x1, y1, dx1, dy1) = (x, y, dx, dy)
    blockers = set()
    while True:
        (r, x2, y2, dx2, dy2) = move(m, x1, y1, dx1, dy1)
        if r < 0:
            return len(blockers)
        elif r > 0:
            t = m[x2][y2]
            m[x2][y2] = '#'
            steps = walk(m, x, y, dx, dy)
            if steps < 0:
                blockers.add((x2, y2))
            m[x2][y2] = t
        (x1, y1, dx1, dy1) = (x2, y2, dx2, dy2)


def print_map(m):
    for l in m:
        print(''.join(l))


area_map = load_input('input.txt')
(x, y) = find_guard(area_map)
(dx, dy) = (-1, 0)  # starting direction is always ^

print('AOC 2024 06 part 1')
print(walk(area_map, x, y, dx, dy))

print()

print('AOC 2024 06 part 2')
print(check_blockers(area_map, x, y, dx, dy))

#!/usr/bin/env python3

import re

WIDTH = 101
HEIGHT = 103
MID_X = (WIDTH - 1) / 2
MID_Y = (HEIGHT - 1) / 2

def load_input(filename):
    robots = []
    with open(filename) as f:
        while line := f.readline().strip():
            m = re.match(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', line)
            robots.append(list(map(int, m.group(1, 2, 3, 4))))
    return robots


def move_robot(r, n):
    (x, y, vx, vy) = r
    return ((x + vx * n) % WIDTH, (y + vy * n) % HEIGHT)


def quadrant(x, y):
    if x < MID_X and y < MID_Y:
        return 1
    elif x > MID_X and y < MID_Y:
        return 2
    elif x < MID_X and y > MID_Y:
        return 3
    elif x > MID_X and y > MID_Y:
        return 4
    return 0


def safety_score(robots, n=100):
    q = [0] * 5
    for r in robots:
        (x, y) = move_robot(r, n)
        q[quadrant(x, y)] += 1
    return q[1] * q[2] * q[3] * q[4]


def layout(robots, n):
    l = [[' '] * WIDTH for h in range(HEIGHT)]
    for r in robots:
        (x, y) = move_robot(r, n)
        l[y][x] = '#'
    print('secs:', n)
    for line in l:
        print(''.join(line))


def xmas_tree(robots):
    for secs in range(WIDTH * HEIGHT):
        if secs % 103 == 18 and secs % 101 == 77:
            layout(robots, secs)


robots = load_input('input.txt')
#robots = load_input('test.txt')

print('AOC 2024 14 part 1')
print(safety_score(robots))

print()

print('AOC 2024 14 part 2')
print(xmas_tree(robots))


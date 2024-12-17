#!/usr/bin/env python3

import re

SPACE = '.'
WALL = '#'
ROBOT = '@'
CRATE = 'O'
CRATE_LEFT = '['
CRATE_RIGHT = ']'

UP = '^'
DOWN = 'v'
LEFT = '<'
RIGHT = '>'
OFFSET = { UP: (-1, 0), RIGHT: (0, 1), DOWN: (1, 0), LEFT: (0, -1) }


def load_input(filename):
    storage = []
    moves = ''
    with open(filename) as f:
        while line := f.readline().strip():
            storage.append(list(line))
        while line := f.readline().strip():
            moves += line
    return (storage, moves)


def print_storage(storage):
    for l in storage:
        print(''.join(l))


def move_robot(storage, rx, ry, move):
    (dx, dy) = OFFSET[move]
    (nrx, nry) = (rx + dx, ry + dy)
    (sx, sy) = (nrx, nry)
    while storage[sx][sy] != SPACE:
        if storage[sx][sy] == WALL:
            return (rx, ry)
        sx += dx
        sy += dy
    if nrx != sx or nry != sy:
        storage[sx][sy] = storage[nrx][nry]
    storage[nrx][nry] = storage[rx][ry]
    storage[rx][ry] = SPACE
    return (nrx, nry)


def move_robot2(storage, rx, ry, move):
    (dx, dy) = OFFSET[move]
    (nx, ny) = (rx + dx, ry + dy)
    if storage[nx][ny] == WALL:
        return (rx, ry)
    if storage[nx][ny] != SPACE:
        if not move_crate2(storage, nx, ny, move, dry_run=True):
            return (rx, ry)
        move_crate2(storage, nx, ny, move)
    storage[nx][ny] = storage[rx][ry]
    storage[rx][ry] = SPACE
    return (nx, ny)


def move_crate2(storage, cx, cy, move, dry_run=False):
    if (move == UP or move == DOWN) and storage[cx][cy] == CRATE_RIGHT:
        # this can only happen when called from move_robot2()
        return move_crate2(storage, cx, cy - 1, move, dry_run)
    (dx, dy) = OFFSET[move]
    if move == UP or move == DOWN:
        if storage[cx + dx][cy + dy] == WALL or storage[cx + dx][cy + dy + 1] == WALL:
            return False
        ok = True
        if ok and storage[cx + dx][cy + dy] == CRATE_LEFT:
            ok = ok and move_crate2(storage, cx + dx, cy + dy, move, dry_run)
        if ok and storage[cx + dx][cy + dy] == CRATE_RIGHT:
            ok = ok and move_crate2(storage, cx + dx, cy + dy - 1, move, dry_run)
        if ok and storage[cx + dx][cy + dy + 1] == CRATE_LEFT:
            ok = ok and move_crate2(storage, cx + dx, cy + dy + 1, move, dry_run)
        if dry_run or not ok:
            return ok
        storage[cx + dx][cy + dy] = storage[cx][cy]
        storage[cx + dx][cy + dy + 1] = storage[cx][cy + 1]
        storage[cx][cy] = SPACE
        storage[cx][cy + 1] = SPACE
        return True
    else:
        if storage[cx + dx][cy + dy] == WALL:
            return False
        ok = True
        if storage[cx + dx][cy + dy] != SPACE:
            ok = ok and move_crate2(storage, cx + dx, cy + dy, move, dry_run)
        if dry_run or not ok:
            return ok
        storage[cx + dx][cy + dy] = storage[cx][cy]
        storage[cx][cy] = SPACE
        return True


def locate_robot(storage):
    for i in range(len(storage)):
        for j in range(len(storage[i])):
            if storage[i][j] == ROBOT:
                return (i, j)
    return None


def apply_moves(storage, moves, move_func=move_robot):
    (x, y) = locate_robot(storage)
    for m in moves:
        (x, y) = move_func(storage, x, y, m)


def sum_crate_gps(storage):
    s = 0
    for i in range(len(storage)):
        for j in range(len(storage[i])):
            if storage[i][j] == CRATE or storage[i][j] == CRATE_LEFT:
                s += 100 * i + j
    return s


def widen_line(l):
    for p in l:
        if p == CRATE:
            yield CRATE_LEFT
            yield CRATE_RIGHT
        elif p == ROBOT:
            yield ROBOT
            yield SPACE
        else:
            yield p
            yield p

(storage, moves) = load_input('input.txt')
#(storage, moves) = load_input('test.txt')

wide_storage = [list(widen_line(l)) for l in storage]

apply_moves(storage, moves)
apply_moves(wide_storage, moves, move_robot2)

#print_storage(storage)
print_storage(wide_storage)

print('AOC 2024 15 part 1')
print(sum_crate_gps(storage))

print()

print('AOC 2024 15 part 2')
print(sum_crate_gps(wide_storage))



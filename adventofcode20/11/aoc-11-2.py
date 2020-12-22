#!/usr/bin/env python3

from copy import deepcopy
from itertools import chain

EMPTY    = 'L'
OCCUPIED = '#'
FLOOR    = '.'

with open('input.txt') as f:
    seats = [list(line.strip()) for line in f.readlines()]

M = len(seats[0])
N = len(seats)

# If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
# If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
# Otherwise, the seat's state does not change.

def check_dir(seats, i, j, di, dj):
    while True:
        i += di
        j += dj
        if i < 0 or j < 0 or i >= N or j >= M:
            return FLOOR
        if seats[i][j] != FLOOR:
            return seats[i][j]

def neighbours(seats, i, j):
    n8 = [check_dir(seats, i, j, -1, -1), check_dir(seats, i, j, -1,  0), check_dir(seats, i, j, -1,  1),
          check_dir(seats, i, j,  0, -1),                                 check_dir(seats, i, j,  0,  1),
          check_dir(seats, i, j,  1, -1), check_dir(seats, i, j,  1,  0), check_dir(seats, i, j,  1,  1)]
    return n8.count(EMPTY), n8.count(OCCUPIED)

change = True
iterations = 0
c_empty, c_occupied = list(chain.from_iterable(seats)).count(EMPTY), list(chain.from_iterable(seats)).count(OCCUPIED)
print(c_empty, c_occupied)
while change:
    iterations += 1
    d_empty, d_occupied = 0, 0
    seats2 = deepcopy(seats)
    for i in range(0, N):
        for j in range(0, M):
            if seats[i][j] == FLOOR:
                continue
            empty, occupied = neighbours(seats, i, j)
            if seats[i][j] == EMPTY and occupied == 0:
                seats2[i][j] = OCCUPIED
                d_occupied += 1
            elif seats[i][j] == OCCUPIED and occupied >= 5:
                seats2[i][j] = EMPTY
                d_empty += 1
    seats = seats2
    change = d_empty > 0 or d_occupied > 0
    c_empty += d_empty - d_occupied
    c_occupied += d_occupied - d_empty
    print(iterations, c_empty, c_occupied)

print('part 2:', c_occupied)

#!/usr/bin/env python3

from copy import deepcopy
from itertools import chain

EMPTY    = 'L'
OCCUPIED = '#'
FLOOR    = '.'

with open('input.txt') as f:
    seats = [[FLOOR] + list(line.strip()) + [FLOOR] for line in f.readlines()]

M = len(seats[0])
seats = [[FLOOR] * M] + seats + [[FLOOR] * M]
N = len(seats)

# If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
# If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
# Otherwise, the seat's state does not change.

def neighbours(seats, i, j):
    n8 = [seats[i-1][j-1], seats[i-1][j], seats[i-1][j+1],
          seats[i][j-1],                  seats[i][j+1],
          seats[i+1][j-1], seats[i+1][j], seats[i+1][j+1]]
    return n8.count(EMPTY), n8.count(OCCUPIED)

change = True
iterations = 0
c_empty, c_occupied = list(chain.from_iterable(seats)).count(EMPTY), list(chain.from_iterable(seats)).count(OCCUPIED)
print(c_empty, c_occupied)
while change:
    iterations += 1
    d_empty, d_occupied = 0, 0
    seats2 = deepcopy(seats)
    for i in range(1, N - 1):
        for j in range(1, M - 1):
            if seats[i][j] == FLOOR:
                continue
            empty, occupied = neighbours(seats, i, j)
            if seats[i][j] == EMPTY and occupied == 0:
                seats2[i][j] = OCCUPIED
                d_occupied += 1
            elif seats[i][j] == OCCUPIED and occupied >= 4:
                seats2[i][j] = EMPTY
                d_empty += 1
    seats = seats2
    change = d_empty > 0 or d_occupied > 0
    c_empty += d_empty - d_occupied
    c_occupied += d_occupied - d_empty
    print(iterations, c_empty, c_occupied)

print('part 1:', c_occupied)

#!/usr/bin/env python3

import re
import sys

forest = []
with open('input.txt') as f:
    for line in f.readlines():
        forest.append(list(line.strip()))

def count_trees(d_col, d_row):
    row, col = (0, 0)
    trees = 0
    while row < len(forest):
        if forest[row][col % len(forest[row])] == '#':
            trees += 1
        row += d_row
        col += d_col
    return trees


print('part 1')
print(count_trees(3, 1))

print('part 2')
c_1_1 = count_trees(1, 1)
c_3_1 = count_trees(3, 1)
c_5_1 = count_trees(5, 1)
c_7_1 = count_trees(7, 1)
c_1_2 = count_trees(1, 2)
print(f'1,1: {c_1_1}')
print(f'3,1: {c_3_1}')
print(f'5,1: {c_5_1}')
print(f'7,1: {c_7_1}')
print(f'1,2: {c_1_2}')
product = c_1_1 * c_3_1 * c_5_1 * c_7_1 * c_1_2
print(f'product: {product}')



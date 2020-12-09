#!/usr/bin/env python3

matrix = []
words = []
with open('matrix.txt') as f:
    for line in f.readlines():
        matrix.append(line.strip())
with open('wordlist.txt') as f:
    for line in f.readlines():
        words.append(line.strip())

all_strings = []
# rows
for s in matrix:
    all_strings.append(s)
    all_strings.append(s[::-1])
# columns
for c in range(len(matrix[0])):
    col = ''.join([row[c] for row in matrix])
    all_strings.append(col)
    all_strings.append(col[::-1])
# diagonals
for d in range(-len(matrix) + 1, len(matrix[0])):
    if d < 0:
        r, c, l = (-d, 0, min(len(matrix) + d, len(matrix[0])))
    else:
        r, c, l = (0, d, min(len(matrix), len(matrix[0]) - d))
    diag1 = ''.join([matrix[r + i][c + i] for i in range(l)])
    diag2 = ''.join([matrix[len(matrix) - r - i - 1][c + i] for i in range(l)])
    all_strings.append(diag1)
    all_strings.append(diag1[::-1])
    all_strings.append(diag2)
    all_strings.append(diag2[::-1])

# check words
missing = []
for w in words:
    for s in all_strings:
        if w in s:
            break
    else:
        missing.append(w)
print(','.join(sorted(missing)))






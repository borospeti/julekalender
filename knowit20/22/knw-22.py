#!/usr/bin/env python3

import re


def check_names(letters, *names):
    letters = list(letters.lower())
    count = 0
    for name in map(str.lower, names):
        try:
            pos = 0
            indices = []
            for c in name:
                np = letters[pos:].index(c)
                indices.append(pos + np)
                pos += np + 1
            for i in indices:
                letters[i] = ''
            count += 1
        except ValueError:
            pass
    return count

best = (0, 0)
with open('input.txt') as f:
    index = 0
    for line in f.readlines():
        count = check_names(*re.sub(r'[\t\[\],]+', ' ', line).strip().split())
        if count > best[1]:
            best = (index, count)
        index += 1
print(best)

#!/usr/bin/env python3

import re
import sys

print('part 1')
count = 0
with open('input.txt') as f:
    group = set()
    for line in f.readlines():
        person = set(re.sub(r'[^a-z]+', '', line))
        group.update(person)
        if len(person) == 0:
            count += len(group)
            group = set()
    count += len(group)
print(f'{count}')


print('part 2')
def count_group(group):
    gs = set(group[0])
    for ps in group[1:]:
        gs.intersection_update(ps)
    return len(gs)

count = 0
with open('input.txt') as f:
    group = []
    for line in f.readlines():
        person = set(re.sub(r'[^a-z]+', '', line))
        if len(person) == 0:
            count += count_group(group)
            group = []
        else:
            group.append(person)
    count += count_group(group)
print(f'{count}')


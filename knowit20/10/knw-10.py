#!/usr/bin/env python3

from collections import defaultdict

points = defaultdict(int)
with open('leker.txt') as f:
    for line in f.readlines():
        for i,p in enumerate(reversed(line.split(','))):
            points[p] += i

vinner = max(points, key=points.get)
print(f'{vinner}-{points.get(vinner)}')




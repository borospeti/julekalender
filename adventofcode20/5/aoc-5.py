#!/usr/bin/env python3

import re
import sys

TRANS = str.maketrans('FBLR', '0101')

max_sid = -1
min_sid = 1024
available = set(range(1024))
with open('input.txt') as f:
    for line in f.readlines():
        seat = line.strip().translate(TRANS)
        #row = int(seat[:7], 2)
        #col = int(seat[7:], 2)
        sid = int(seat, 2)
        max_sid = max(sid, max_sid)
        min_sid = min(sid, max_sid)
        available.remove(sid)
available -= set(range(0, min_sid))
available -= set(range(max_sid + 1, 1024))

print('part 1')
print(max_sid)

print('part 2')
print(available)





#!/usr/bin/env python3

import re
from collections import defaultdict

with open('family.txt') as f:
    family = re.sub(r'([()])', r' \1 ', f.read()).split()

level = 0
ancestors = defaultdict(int)
for token in family:
    if token == '(':
        level += 1
    elif token == ')':
        level -= 1
    else:
        ancestors[level] += 1
print(max(ancestors.values()))

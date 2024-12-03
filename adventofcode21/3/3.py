#!/usr/bin/env python3

from functools import reduce

with open('input.txt') as input:
    data = [[int(x) for x in list(line.strip())] for line in input]

#
# part 1
#
s = reduce(lambda x, y:  [sum(a) for a in zip(x, y)], data)
gamma = int(''.join(['0' if x < len(data) / 2 else '1' for x in s]), 2)
epsilon = int(''.join(['1' if x < len(data) / 2 else '0' for x in s]), 2)
print(s, len(data) / 2, gamma, epsilon, gamma * epsilon)

#
# part 2
#
def select(l, most_common=True, n=0):
    if len(l) == 1:
        return l[0]
    s = sum([x[n] for x in l])
    b = 1 if (most_common and s >= len(l) / 2) or (not most_common and s < len(l) / 2) else 0
    return select([x for x in l if x[n] == b], most_common, n + 1)

oxy = int(''.join([str(x) for x in select(data)]), 2)
co2 = int(''.join([str(x) for x in select(data, False)]), 2)

print(oxy, co2, oxy * co2)


#!/usr/bin/env python3

with open('input.txt') as f:
    numbers = set([int(x) for x in f.readlines()])

print('part 1')

def sum_of_two(ns):
    for n in ns:
        if 2020 - n in ns:
            return (n, 2020 - n, n * (2020 - n))
    return None

print(sum_of_two(numbers))


print('part 2')

def sum_of_three(ns_s):
    ns = sorted(list(ns_s), reverse=True)
    for i in range(len(ns) - 2):
        for j in range(i + 1, len(ns) - 1):
            for k in range(j + 1, len(ns)):
                if ns[i] + ns[j] + ns[k] == 2020:
                    return (ns[i], ns[j], ns[k], ns[i] * ns[j] * ns[k])
    return None

print(sum_of_three(numbers))

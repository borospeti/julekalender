#!/usr/bin/env python3

with open('input.txt') as f:
    timestamp = int(f.readline())
    buses = [int(bus if bus != 'x' else '0') for bus in f.readline().split(',')]

print('part 1')
best = (None, max(buses))
for bus in buses:
    if bus == 0:
        continue
    wait = (bus - (timestamp % bus)) % bus
    if wait < best[1]:
        best = (bus, wait)
print(best, best[0] * best[1])


print('part 2')
# https://en.wikipedia.org/wiki/Chinese_remainder_theorem

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = egcd(b % a, a)
        return (gcd, y - (b//a) * x, x)

def chinese_2(a1, n1, a2, n2):
    gcd, m1, m2 = egcd(n1, n2)
    if gcd != 1:
        raise Exception(f'{n1} and {n2} are not coprimes')
    x, y = a1 + (a2 - a1) * m1 * n1, n1 * n2
    return (x % y, y)

def chinese_n(l):
    if len(l) == 1:
        return l[0]
    return chinese_2(*l[0], *chinese_n(l[1:]))

rems = [((x[1] - x[0]) % x[1], x[1]) for x in filter(lambda b: b[1] > 0, enumerate(buses))]
print(chinese_n(rems))


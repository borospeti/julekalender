#!/usr/bin/env python3

# solution: 705

from itertools import chain, combinations
from math import prod, sqrt

N = 1000000

primes = 2 * [False] + (N - 1) * [True]
for i in range(2, int(N ** 0.5 + 1.5)):
    if primes[i]:
        for j in range(i * i, N + 1, i):
            primes[j] = False
primes = [n for n, p in enumerate(primes) if p]

def factorise(n):
    factors = []
    i = 0
    while n > 1:
        p = primes[i]
        while n % p == 0:
            factors.append(p)
            n = n // p
        i += 1
    return factors

def divisors(n):
    divs = {1, n}
    factors = factorise(n)
    for fs in chain.from_iterable(combinations(factors, r) for r in range(len(factors) + 1)):
        if fs:
            divs.add(prod(fs))
    return divs

def is_rich(n):
    return sum(divisors(n)) > 2 * n

def is_rich_and_square_diff(n):
    sd = sum(divisors(n)) - 2 * n
    if sd <= 0:
        return False
    print(f'{n}?')
    return sd == int(sqrt(sd)) ** 2

all_rasd = [n for n in range(1, N + 1) if is_rich_and_square_diff(n)]
print(all_rasd)
print(len(all_rasd))




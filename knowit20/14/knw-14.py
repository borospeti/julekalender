#!/usr/bin/env python3

N = 1800813

class PlusMinusSequence:
    def __init__(self):
        self.sequence = []
        self.sequence_set = set()
        self.n = 0
        self.maximum = 0
        self._add(0)
        self._add(1)

    def _add(self, value):
        self.sequence.append(value)
        self.sequence_set.add(value)
        self.n += 1
        if value > self.maximum:
            self.maximum = value

    def _next(self):
        value = self.sequence[-2] - self.n
        if value > 0 and value not in self.sequence_set:
            self._add(value)
        else:
            self._add(self.sequence[-2] + self.n)

    def generate(self, m):
        while self.n < m:
            self._next()

pms = PlusMinusSequence()
pms.generate(N)


M = pms.maximum
primes = 2 * [False] + (M - 1) * [True]
for i in range(2, int(M ** 0.5 + 1.5)):
    if primes[i]:
        for j in range(i * i, M + 1, i):
            primes[j] = False

unique_prime_count = 0
for v in pms.sequence_set:
    if primes[v]:
        unique_prime_count += 1
prime_count = 0
for v in pms.sequence:
    if primes[v]:
        prime_count += 1

print(prime_count, unique_prime_count)

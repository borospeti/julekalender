#!/usr/bin/env python3

import sys


# Julenissen hater av en eller annen grunn sifferet 7, og reagerer
# sterkt når han ser en pakke med dette sifferet. Hans reaksjon er at
# han kaster pakken i søpla, og i ukontrollert sinne også kaster de P
# neste pakkene, hvor P er nærmeste primtall som er mindre eller lik
# tallet på pakken.
#
# Oppgave
#
# Julenissen skal levere pakker til alle de snille barna i
# Norge. Terskelen er ganske lav for hva Julenissen anser som et snilt
# barn, vi er alle snille barn i Julenissens øyne. Dvs. hele norges
# befolkning på 5433000, skal få en pakke levert. Hvor mange av disse
# pakkene vil faktisk bli levert?

N = 5433000

primes = 2 * [False] + (N - 1) * [True]
for i in range(2, int(N ** 0.5 + 1.5)):
    if primes[i]:
        for j in range(i * i, N + 1, i):
            primes[j] = False

n = 0
count = 0
while n < N:
    if '7' not in str(n):
        count += 1
        n += 1
        continue
    p = n
    while not primes[p]:
        p -= 1
    n += 1 + p

print(count)



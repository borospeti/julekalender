#!/usr/bin/env python3

#real:
a = 10212254
b = 12577395

#test:
#a = 5764801
#b = 17807724

i = 2
q = 20201227
n = 1
c = 0
while i > 0:
    if n == a:
        ac = c
        i -= 1
    if n == b:
        bc = c
        i -= 1
    n = (7 * n) % q
    c += 1

print(ac, bc)

n = 1
for i in range(bc):
    n = (a * n) % q
print(n)

n = 1
for i in range(ac):
    n = (b * n) % q
print(n)


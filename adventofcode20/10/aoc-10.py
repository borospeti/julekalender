#!/usr/bin/env python3

with open('input.txt') as f:
    numbers = sorted([int(line) for line in f.readlines()])

numbers = [0] + numbers + [numbers[-1] + 3]
differences = [a - b for (a, b) in zip(numbers[1:], numbers[:-1])]
print('part 1')
print(differences.count(1) * differences.count(3))

n = len(numbers)
valid = [0] * (n -1) + [1]
for i in range(n - 2, -1, -1):
    j = i + 1
    while j < n and numbers[j] - numbers[i] <= 3:
        valid[i] += valid[j]
        j += 1
print('part 2')
print(valid[0])

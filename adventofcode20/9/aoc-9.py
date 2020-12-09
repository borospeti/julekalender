#!/usr/bin/env python3

import re
import sys

with open('input.txt') as f:
    numbers = [int(line) for line in f.readlines()]

def is_invalid_at(i):
    for j in range(i - 25, i - 1):
        for k in range(j + 1, i):
            if numbers[j] + numbers[k] == numbers[i]:
                return False
    return True

print('part 1')
PREAMBLE = 25
invalid = None
for i in range(25, len(numbers)):
    if is_invalid_at(i):
        invalid = numbers[i]
        print(f'invalid: {invalid} at pos {i}')
        break

print('part 2')
start = 0
end = 0
current = 0
while end < len(numbers):
    if current == invalid and end - start > 1:
        print(f'continuous range: [{start}, {end})')
        print(f'weakness: {min(numbers[start:end]) + max(numbers[start:end])}')

    if current >= invalid:
        current -= numbers[start]
        start += 1
    else:
        current += numbers[end]
        end += 1


#!/usr/bin/env python3

import re
import sys

passwords = []
with open('input.txt') as f:
    for line in f.readlines():
        m = re.match(r'(\d+)-(\d+)\s+(\w):\s*(\w+)', line.strip())
        if m is None:
            print('unparable line:', line)
            sys.exit(1)
        passwords.append((int(m.group(1)), int(m.group(2)), m.group(3), m.group(4)))


print('part 1')
valid, invalid = (0, 0)
for (low, high, char, password) in passwords:
    if low <= password.count(char) <= high:
        valid +=1
    else:
        invalid += 1
print(f'valid: {valid}, invalid: {invalid}')


print('part 2')
valid, invalid = (0, 0)
for (first, second, char, password) in passwords:
    try:
        if (password[first - 1] == char) != (password[second - 1] == char):
            valid +=1
        else:
            invalid += 1
    except Error as e:
        print(e)
        sys.exit(1)
print(f'valid: {valid}, invalid: {invalid}')





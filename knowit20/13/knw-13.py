#!/usr/bin/env python3

from collections import defaultdict

with open('text.txt') as f:
    text = list(f.read().strip())

freq = defaultdict(int)
output = []
for letter in text:
    if freq[letter] == ord(letter) - ord('a'):
        output.append(letter)
    freq[letter] += 1
print(''.join(output))

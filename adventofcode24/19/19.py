#!/usr/bin/env python3

import re


def load_input(filename):
    patterns = []
    with open(filename) as f:
        towels = [t.strip() for t in f.readline().split(',')]
        f.readline()  # skip empty line
        while line := f.readline().strip():
            patterns.append(line)
    return (towels, patterns)


class DesignCounter:
    def __init__(self, towels):
        self._cleaned = []
        checker = re.compile(r'^thiswillnotmatch$')
        for towel in sorted(towels, key=len):
            if not checker.match(towel):
                self._cleaned.append(towel)
                checker = re.compile(r'^(' + r'|'.join(self._cleaned) + r')*$')
        self._checker = checker
        self._towels = set(towels)
        self._split_threshold = 2 * max(len(t) for t in self._towels)
        self._pattern_cache = {}

    def count_designs(self, pattern):
        if len(pattern) == 0:
            return 1
        if pattern in self._pattern_cache:
            return self._pattern_cache[pattern]
        if not self._checker.match(pattern):
            self._pattern_cache[pattern] = 0
            return 0
        designs = 0
        if len(pattern) < self._split_threshold:
            for t in self._towels:
                if pattern.startswith(t):
                    designs += self.count_designs(pattern[len(t):])
        else:
            mid = len(pattern) // 2
            designs += self.count_designs(pattern[:mid]) * self.count_designs(pattern[mid:])
            for i in range(2, 9):
                for j in range(1, i):
                    if pattern[mid-j:mid+i-j] in self._towels:
                        designs += self.count_designs(pattern[:mid-j]) * self.count_designs(pattern[mid+i-j:])
        self._pattern_cache[pattern] = designs
        return designs

    def count_possible_patterns(self, patterns):
        return sum(1 for pattern in patterns if self._checker.match(pattern))

    def count_all_designs(self, patterns):
        return sum(self.count_designs(pattern) for pattern in patterns)


(towels, patterns) = load_input('input.txt')
counter = DesignCounter(towels)

print('AOC 2024 19 part 1')
print(counter.count_possible_patterns(patterns))

print()

print('AOC 2024 19 part 2')
print(counter.count_all_designs(patterns))



#!/usr/bin/env python3

class Riddle:
    def __init__(self, left, right):
        self._left = left
        self._right = right
        self._left_candidates = set()
        self._right_candidates = set()

    def check(self, word):
        if len(word) > len(self._left) and word.startswith(self._left):
            self._left_candidates.add(word[len(self._left):])
        if len(word) > len(self._right) and word.endswith(self._right):
            self._right_candidates.add(word[:-len(self._right)])

    def glue_words(self):
        return self._left_candidates & self._right_candidates

    def __str__(self):
        return f'{self._left} {self._right} {self.glue_words()}'


with open('wordlist.txt') as f:
    words = set([line.strip() for line in f.readlines()])
with open('riddles.txt') as f:
    riddles = [Riddle(*line.strip().split(', ')) for line in f.readlines()]

all_glue_words = set()
for riddle in riddles:
    for word in words:
        riddle.check(word)
    print(riddle)
    all_glue_words |= riddle.glue_words()
print(sum([len(x) for x in all_glue_words & words]))

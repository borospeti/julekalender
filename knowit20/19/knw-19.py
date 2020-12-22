#!/usr/bin/env python3

import re
from copy import deepcopy
from collections import defaultdict

class ChairGame:
    def __init__(self, rule, shift, *args):
        self.rule = int(rule)
        self.shift = int(shift)
        self.participants = list(args)
        self._current = None
        self._remove = 0

    def _do_shift(self):
        s = self.shift % len(self._current)
        self._current = self._current[-s:] + self._current[:-s]

    def _do_remove(self):
        if self.rule == 1:
            self._current = self._current[1:]
        elif self.rule == 4:
            self._current = self._current[:-1]
        elif self.rule == 2:
            if self._remove >= len(self._current):
                self._remove = 0
            self._current = self._current[:self._remove] + self._current[self._remove+1:]
            self._remove += 1
        elif self.rule == 3:
            m = len(self._current)
            if m < 3:
                self._current = self._current[1:]
            elif m % 2 == 0:
                self._current = self._current[:m//2 - 1] + self._current[m//2 + 1:]
            else:
                self._current = self._current[:m//2] + self._current[m//2 + 1:]
        else:
            raise Exception(f'unknown rule: {self.rule}')

    def _do_round(self):
        self._do_shift()
        self._do_remove()

    def play(self):
        self._current = deepcopy(self.participants)
        while len(self._current) > 1:
            self._do_round()
        return self._current[0]

#print(ChairGame('1', '3', 'Jenny', 'Alvin', 'Greger', 'Petra', 'Olaug', 'Olaf').play())
#print(ChairGame('2', '3', 'Jenny', 'Alvin', 'Greger', 'Petra', 'Olaug', 'Olaf').play())
#print(ChairGame('3', '3', 'Jenny', 'Alvin', 'Greger', 'Petra', 'Olaug').play())
#print(ChairGame('4', '3', 'Jenny', 'Alvin', 'Greger', 'Petra', 'Olaug', 'Olaf').play())

games = []
with open('input.txt') as f:
    for line in f.readlines():
        games.append(ChairGame(*re.sub(r'[\t\[\],]+', ' ', line).strip().split()))

winners = defaultdict(int)
for game in games:
    winners[game.play()] += 1
print(max(winners, key=winners.get))

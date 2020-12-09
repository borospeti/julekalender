#!/usr/bin/env python3

from copy import deepcopy

class Grid:
    def __init__(self):
        with open('elves.txt') as f:
            self._elves = [list(line.strip()) for line in f.readlines()]

    def sick_neighbours(self, x, y):
        cnt = 0
        if x > 0 and self._elves[y][x - 1] == 'S':
            cnt += 1
        if x < len(self._elves[y]) - 1 and self._elves[y][x + 1] == 'S':
            cnt += 1
        if y > 0 and self._elves[y - 1][x] == 'S':
            cnt += 1
        if y < len(self._elves) - 1 and self._elves[y + 1][x] == 'S':
            cnt += 1
        return cnt

    def update(self):
        elves2 = deepcopy(self._elves)
        changed = False
        for y in range(len(elves2)):
            for x in range(len(elves2[y])):
                if elves2[y][x] == 'F' and self.sick_neighbours(x, y) >= 2:
                    elves2[y][x] = 'S'
                    changed = True
        self._elves = elves2
        return changed

    def run(self):
        days = 0
        while self.update():
            days += 1
        return days

grid = Grid()
print(grid.run() + 1)



#!/usr/bin/env python3


class Topomap:
    def __init__(self, filename):
        self.TRAILHEAD = 0
        self.PEAK = 9
        self._load_input(filename)

    def _load_input(self, filename):
        self._topomap = []
        with open(filename) as f:
            for line in f:
                self._topomap.append(list(map(int, line.strip())))
        self._height = len(self._topomap)
        self._width = len(self._topomap[0])

    def find_trailheads(self):
        for x in range(self._height):
            for y in range(self._width):
                if self._topomap[x][y] == self.TRAILHEAD:
                    yield (x, y)

    def available_moves(self, x, y):
        current = self._topomap[x][y]
        for (dx, dy) in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            if 0 <= x + dx < self._height and 0 <= y + dy < self._width and self._topomap[x + dx][y + dy] == current + 1:
                yield (x + dx, y + dy)

    def trace_trails(self, x, y):
        if self._topomap[x][y] == self.PEAK:
            yield (x, y)
        for (x2, y2) in self.available_moves(x, y):
            yield from self.trace_trails(x2, y2)

    def find_trails(self, all_trails=False):
        score = 0
        for (x, y) in self.find_trailheads():
            trails = self.trace_trails(x, y)
            if (all_trails):
                score += len(list(trails))
            else:
                score += len(set(trails))
        return score


topomap = Topomap('input.txt')

print('AOC 2024 10 part 1')
print(topomap.find_trails())

print()

print('AOC 2024 10 part 2')
print(topomap.find_trails(all_trails=True))




#!/usr/bin/env python3

import re

class Location():
    def __init__(self, name, x, y):
        self._name = name
        self._x = x
        self._y = y
        self._time = 0.00

    def time(self):
        return self._time

    def update_time(self, nisse_pos):
        dx, dy = self._x - nisse_pos[0], self._y - nisse_pos[1]
        # Taxicab geometry:
        distance = abs(dx) + abs(dy)
        if distance >= 50:
            self._time += 1.00
        elif distance >= 20:
            self._time += 0.75
        elif distance >= 5:
            self._time += 0.50
        elif distance > 0:
            self._time += 0.25
        # Normal geometry:
        # distance = dx * dx + dy * dy
        # if distance >= 2500:
        #     self._time += 1.00
        # elif distance >= 400:
        #     self._time += 0.75
        # elif distance >= 25:
        #     self._time += 0.50
        # elif distance > 0:
        #     self._time += 0.25

    def pos(self):
        return (self._x, self._y)

    def __str__(self):
        return f'{self._name}: ({self._x}, {self._y}) [{self._time:0.2f}]'

class Nisse():
    def __init__(self):
        self._x = 0
        self._y = 0

    def pos(self):
        return (self._x, self._y)

    def move(self, dest):
        x, y = dest
        dx = 1 if x > self._x else -1
        dy = 1 if y > self._y else -1
        while self._x != x:
            self._x += dx
            yield(self.pos())
        while self._y != y:
            self._y += dy
            yield(self.pos())

    def __str__(self):
        return f'Nisse: ({self._x}, {self._y})'


locations = {}
route = []
with open('input.txt') as f:
    for line in f.readlines():
        m = re.fullmatch(r'([^:]+):\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*', line)
        if m:
            locations[m.group(1)] = Location(m.group(1), int(m.group(2)), int(m.group(3)))
        else:
            route.append(line.strip())

nisse = Nisse()

for nxt in route:
    nxt_loc = locations[nxt]
    for pos in nisse.move(nxt_loc.pos()):
        for loc in locations.values():
            loc.update_time(pos)

#print(nisse)
#for l in locations.values():
#    print(l)

min_loc = min(locations.values(), key = Location.time)
max_loc = max(locations.values(), key = Location.time)

print(f'Min loc time: {min_loc}')
print(f'Max loc time: {max_loc}')
print(f'Time difference: {max_loc.time() - min_loc.time()}')

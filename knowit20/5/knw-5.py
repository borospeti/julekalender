#!/usr/bin/env python3

from itertools import groupby
from matplotlib import pyplot as plt

class Mus:
    def __init__(self):
        self.OFFSET = {'O':(0,1), 'N':(0,-1), 'H':(1,0), 'V':(-1,0)}
        self._pos = (0,0)
    def move(self, d, s):
        self._pos = (self._pos[0] + self.OFFSET[d][0] * s, self._pos[1] + self.OFFSET[d][1] * s)
        return self._pos

with open('rute.txt') as f:
    mus = Mus()
    rute = [mus.move(k, len(list(g))) for k, g in groupby(f.read())]

print(sum([p1[0]*p2[1] - p2[0]*p1[1] for p1, p2 in zip(rute, rute[1:] + rute[:1])]) / 2)

plt.fill([p[0] for p in rute], [p[1] for p in rute], color='slategrey')
plt.show()

#!/usr/bin/env python3

import numpy as np
from scipy.signal import fftconvolve

# If a cube is active and exactly 2 or 3 of its neighbors are also
# active, the cube remains active. Otherwise, the cube becomes
# inactive.

# If a cube is inactive but exactly 3 of its neighbors are active, the
# cube becomes active. Otherwise, the cube remains inactive.

class ConwayCube:
    ACTIVE   = '#'
    INACTIVE = '.'

    def __init__(self, dim=3):
        self.grid = None
        self.dim = dim
        if dim == 3:
            self.kernel = np.ones((3,3,3))
            self.kernel[1,1,1] = 0
        elif dim == 4:
            self.kernel = np.ones((3,3,3,3))
            self.kernel[1,1,1,1] = 0
        else:
            raise Excteption(f'Unsupported number of dimensions')

    def load(self, filename):
        with open(filename) as f:
            init = [line.strip() for line in f.readlines()]
        if self.dim == 3:
            self.grid = np.rint(np.zeros((len(init[0]), len(init), 1)))
        else:
            self.grid = np.rint(np.zeros((len(init[0]), len(init), 1, 1)))
        for y in range(len(init)):
            for x in range(len(init[y])):
                if init[y][x] == self.ACTIVE:
                    if self.dim == 3:
                        self.grid[x, y, 0] = 1
                    else:
                        self.grid[x, y, 0, 0] = 1

    def cycle(self):
        extended = np.pad(self.grid, 1)
        convolved = fftconvolve(extended, self.kernel, mode='same')
        for idx, v in np.ndenumerate(extended):
            active = round(float(v))
            neighbours = round(float(convolved[idx]))
            if active == 1 and (neighbours < 2 or neighbours > 3):
                extended[idx] = 0
            elif active == 0 and neighbours == 3:
                extended[idx] = 1
        self.grid = extended

    def count_active(self):
        return round(float(np.sum(self.grid)))

print('part 1')
cube = ConwayCube()
cube.load('input.txt')
for i in range(6):
    cube.cycle()
print(cube.count_active())

print('part 2')
cube = ConwayCube(4)
cube.load('input.txt')
for i in range(6):
    cube.cycle()
print(cube.count_active())

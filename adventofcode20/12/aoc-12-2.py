#!/usr/bin/env python3


class Ship:
    def __init__(self):
        self.north = 0
        self.east = 0
        self.wpt_north = 1
        self.wpt_east = 10
        self.instuctions = []

    def read_instructions(self, filename):
        with open(filename) as f:
            self.instructions = [(line[0], int(line.strip()[1:])) for line in f.readlines()]

    def rotate_wpt(self, angle):
        q = (angle // 90) % 4
        if q == 1:
            self.wpt_north, self.wpt_east = -self.wpt_east, self.wpt_north
        elif q == 2:
            self.wpt_north, self.wpt_east = -self.wpt_north, -self.wpt_east
        elif q == 3:
            self.wpt_north, self.wpt_east = self.wpt_east, -self.wpt_north

    def execute(self, inst):
        op, param = inst
        if op == 'F':
            self.north += self.wpt_north * param
            self.east += self.wpt_east * param
        elif op == 'E':
            self.wpt_east += param
        elif op == 'W':
            self.wpt_east -= param
        elif op == 'N':
            self.wpt_north += param
        elif op == 'S':
            self.wpt_north -= param
        elif op == 'R':
            self.rotate_wpt(param)
        elif op == 'L':
            self.rotate_wpt(-param)

    def run(self):
        for inst in self.instructions:
            self.execute(inst)
        print(f'e:{self.east} n:{self.north} d:{abs(self.east) + abs(self.north)}')



ship = Ship()
ship.read_instructions('input.txt')
print('part 2')
ship.run()

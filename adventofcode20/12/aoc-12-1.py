#!/usr/bin/env python3


class Ship:
    DIRECTIONS = ['E', 'S', 'W', 'N']

    def __init__(self):
        self.heading = 0
        self.north = 0
        self.east = 0
        self.instuctions = []

    def read_instructions(self, filename):
        with open(filename) as f:
            self.instructions = [(line[0], int(line.strip()[1:])) for line in f.readlines()]

    def execute(self, inst):
        op, param = inst
        if op == 'F':
            op = self.DIRECTIONS[self.heading]
        if op == 'E':
            self.east += param
        elif op == 'W':
            self.east -= param
        elif op == 'N':
            self.north += param
        elif op == 'S':
            self.north -= param
        elif op == 'R':
            self.heading = (self.heading + param // 90) % 4
        elif op == 'L':
            self.heading = (self.heading - param // 90) % 4

    def run(self):
        for inst in self.instructions:
            self.execute(inst)
        print(f'h:{self.DIRECTIONS[self.heading]} e:{self.east} n:{self.north} d:{abs(self.east) + abs(self.north)}')



ship = Ship()
ship.read_instructions('input.txt')
print('part 1')
ship.run()

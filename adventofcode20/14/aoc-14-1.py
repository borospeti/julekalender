#!/usr/bin/env python3

import re

print('part 1')

class Computer:
    WORD_SIZE = 36
    def __init__(self):
        self.code = []
        self.memory = {}
        self.and_mask = 2 ** self.WORD_SIZE - 1
        self.or_mask = 0

    def load(self, filename):
        with open(filename) as f:
            self.code = [''.join(line.split()) for line in f.readlines()]

    def set_mask(self, mask):
        self.and_mask = int(mask.replace('X', '1'), 2)
        self.or_mask = int(mask.replace('X', '0'), 2)

    def set_memory(self, addr, data):
        self.memory[addr] = (data & self.and_mask) | self.or_mask

    def execute(self, line):
        m = re.fullmatch(r'mask=([01X]+)|mem\[(\d+)\]=(\d+)', line)
        if not m:
            raise Exception(f'invalid instruction: {line}')
        if m.group(1):
            self.set_mask(m.group(1))
        else:
            self.set_memory(int(m.group(2)), int(m.group(3)))

    def run(self):
        for line in self.code:
            self.execute(line)

    def sum_memory(self):
        return sum(self.memory.values())

computer = Computer()
computer.load('input.txt')
computer.run()
print(computer.sum_memory())

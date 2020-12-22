#!/usr/bin/env python3

import re
from itertools import chain, combinations
from functools import reduce

def powerset(l):
    return chain.from_iterable(combinations(l, r) for r in range(len(l) + 1))

print('part 2')

class Computer:
    WORD_SIZE = 36
    def __init__(self):
        self.code = []
        self.memory = {}
        self.and_mask = 2 ** self.WORD_SIZE - 1
        self.or_mask = 0
        self.floating = []

    def load(self, filename):
        with open(filename) as f:
            self.code = [''.join(line.split()) for line in f.readlines()]

    def set_mask(self, mask):
        self.or_mask = int(mask.replace('X', '0'), 2)
        self.and_mask = int(mask.replace('0', '1').replace('X', '0'), 2)
        self.floating = [2 ** i for i, b in enumerate(mask[::-1]) if b == 'X']

    def set_memory(self, addr, data):
        self.memory[addr] = data

    def mask_address(self, addr):
        addr = (addr & self.and_mask) | self.or_mask
        for floating in chain.from_iterable(combinations(self.floating, r) for r in range(len(self.floating) + 1)):
            yield addr | reduce(lambda a, b: a | b, floating, 0)

    def set_memory_masked(self, addr, data):
        for floating_addr in self.mask_address(addr):
            self.memory[floating_addr] = data

    def execute(self, line):
        m = re.fullmatch(r'mask=([01X]+)|mem\[(\d+)\]=(\d+)', line)
        if not m:
            raise Exception(f'invalid instruction: {line}')
        if m.group(1):
            self.set_mask(m.group(1))
        else:
            self.set_memory_masked(int(m.group(2)), int(m.group(3)))

    def run(self):
        for line in self.code:
            self.execute(line)

    def sum_memory(self):
        return sum(self.memory.values())

computer = Computer()
computer.load('input.txt')
computer.run()
print(computer.sum_memory())

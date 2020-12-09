#!/usr/bin/env python3

import re
import sys

class VMError(Exception):
    pass

class VM():
    def __init__(self):
        with open('input.txt') as f:
            self.instructions = [line.split() for line in f.readlines()]
        self.acc = 0
        self.pc = 0
        self.visited = [False for i in self.instructions]
        self.patched = None

    def size(self):
        return len(self.instructions)

    def reset(self, patch=None):
        self.acc = 0
        self.pc = 0
        self.visited = [False for i in self.instructions]
        self.patched = patch

    def patch(self, opcode):
        if self.pc == self.patched:
            if opcode == 'nop':
                return 'jmp'
            elif opcode == 'jmp':
                return 'nop'
        return opcode

    def step(self):
        if self.pc < 0 or self.pc > len(self.instructions):
            raise VMError(f'invalid address pc={self.pc}')
        if self.pc == len(self.instructions):
            return True, f'program terminated normally, pc={self.pc}, acc={self.acc}'
        if self.visited[self.pc]:
            raise VMError(f'infinite loop detected at pc={self.pc}, acc={self.acc}')
        self.visited[self.pc] = True
        opcode, operand = self.instructions[self.pc]
        opcode = self.patch(opcode)
        if opcode == 'acc':
            self.acc += int(operand)
            self.pc += 1
        elif opcode == 'jmp':
            self.pc += int(operand)
        elif opcode == 'nop':
            self.pc += 1
        else:
            raise VMError(f'invalid instruction opcode={opcode} at ps={self.pc}')
        return False, f'pc={self.pc}, acc={self.acc}'

    def run(self):
        while True:
            status, message = self.step()
            if status:
                return message

vm = VM()

print('part 1')
try:
    print(vm.run())
except VMError as e:
    print(e)

print('part 1')
for i in range(vm.size()):
    vm.reset(i)
    try:
        print(f'patch at pc={i}:', vm.run())
    except VMError:
        pass

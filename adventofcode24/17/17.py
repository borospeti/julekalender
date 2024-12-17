#!/usr/bin/env python3

import re
from itertools import batched


class ChronospatialComputer:
    def __init__(self):
        self._instructions = [ self._adv, self._bxl, self._bst, self._jnz, self._bxc, self._out, self._bdv, self._cdv ]
        self._mnemonic = [ 'adv', 'bxl', 'bst', 'jnz', 'bxc', 'out', 'bdv', 'cdv' ]
        self._program = []
        self._registers = { 'A': 0, 'B': 0, 'C': 0 }
        self._pc = 0

    def load(self, filename):
        program = []
        with open(filename) as f:
            for line in f:
                line = line.strip()
                if m := re.match(r'Register ([A-C]): (\d+)', line):
                    self._registers[m.group(1)] = int(m.group(2))
                elif m := re.match(r'Program: (.*)', line):
                    self._program = list(map(int, m.group(1).split(',')))
                    self._pc = 0

    def dump(self):
        print('Program: ', self._program)
        print('PC: ', self._pc)
        print('Registers: ', self._registers)

    def get_program(self):
        return ','.join(map(str, self._program))

    def get_assembly(self):
        for (m, o) in batched(self._program, 2):
            print(self._mnemonic[m], o)

    def _combo(self, n):
        match n:
            case n if n <= 3:
                return n
            case 4:
                return self._registers['A']
            case 5:
                return self._registers['B']
            case 6:
                return self._registers['C']
            case 7:
                raise Error('Invalid combo operand')

    def _div(self, register, operand):
        numerator = self._registers['A']
        denominator = self._combo(operand)
        self._registers[register] = numerator >> denominator
        yield from ()

    # The adv instruction (opcode 0) performs division. The numerator is
    # the value in the A register. The denominator is found by raising 2
    # to the power of the instruction's combo operand. (So, an operand of
    # 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)
    # The result of the division operation is truncated to an integer and
    # then written to the A register.
    def _adv(self, operand):
        yield from self._div('A', operand)

    # The bxl instruction (opcode 1) calculates the bitwise XOR of
    # register B and the instruction's literal operand, then stores the
    # result in register B.
    def _bxl(self, operand):
        self._registers['B'] ^= operand
        yield from ()

    # The bst instruction (opcode 2) calculates the value of its combo
    # operand modulo 8 (thereby keeping only its lowest 3 bits), then
    # writes that value to the B register.
    def _bst(self, operand):
        self._registers['B'] = self._combo(operand) & 7
        yield from ()

    # The jnz instruction (opcode 3) does nothing if the A register is
    # 0. However, if the A register is not zero, it jumps by setting the
    # instruction pointer to the value of its literal operand; if this
    # instruction jumps, the instruction pointer is not increased by 2
    # after this instruction.
    def _jnz(self, operand):
        if self._registers['A'] != 0:
            self._pc = operand
        yield from ()

    # The bxc instruction (opcode 4) calculates the bitwise XOR of
    # register B and register C, then stores the result in register
    # B. (For legacy reasons, this instruction reads an operand but
    # ignores it.)
    def _bxc(self, operand):
        self._registers['B'] ^= self._registers['C']
        yield from ()

    # The out instruction (opcode 5) calculates the value of its combo
    # operand modulo 8, then outputs that value. (If a program outputs
    # multiple values, they are separated by commas.)
    def _out(self, operand):
        # print(oct(self._registers['A']), oct(self._registers['B']), oct(self._registers['C']))
        yield self._combo(operand) & 7

    # The bdv instruction (opcode 6) works exactly like the adv
    # instruction except that the result is stored in the B register. (The
    # numerator is still read from the A register.)
    def _bdv(self, operand):
        yield from self._div('B', operand)

    # The cdv instruction (opcode 7) works exactly like the adv
    # instruction except that the result is stored in the C register. (The
    # numerator is still read from the A register.)
    def _cdv(self, operand):
        yield from self._div('C', operand)

    def _exec(self):
        opcode = self._program[self._pc]
        operand = self._program[self._pc + 1]
        self._pc += 2
        yield from self._instructions[opcode](operand)

    def step(self):
        if self._pc < len(self._program):
            yield from self._exec()

    def run(self):
        while self._pc < len(self._program):
            yield from self._exec()

    def full_run(self):
        return ','.join(map(str, self.run()))

    def reset(self, a=0):
        self._pc = 0
        self._registers['A'] = a
        self._registers['B'] = 0
        self._registers['C'] = 0

    def _find_a_internal(self, target, current):
        for d in range(0 if current > 0 else 1, 8):
            n = (current << 3) + d
            self.reset(n)
            r = self.full_run()
            if len(r) > len(target):
                break
            if target == r:
                yield n
            elif target.endswith(r):
                yield from self._find_a_internal(target, n)

    def find_a(self):
        return next(self._find_a_internal(self.get_program(), 0))


computer =  ChronospatialComputer()
computer.load('input.txt')
#computer.load('test.txt')
#computer.dump()
#computer.get_assembly()

print('AOC 2024 17 part 1')
print(computer.full_run())

print()

print('AOC 2024 17 part 2')
print(computer.find_a())

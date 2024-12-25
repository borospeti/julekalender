#!/usr/bin/env python3

from itertools import product


def load_input(filename):
    codes = []
    with open(filename) as f:
        for line in f:
            codes.append(line.strip())
    return codes


class Keypad:
    def __init__(self, keys):
        self._keys = keys
        self._height = len(keys)
        self._width = len(keys[0])
        self._transitions = self._generate_transitions()
        self._cache = {}
        self._filled = 0

    def _generate_transitions(self):
        transitions = {}
        for start in product(range(self._height), range(self._width)):
            if self.key(start) == 'X':
                continue
            for end in product(range(self._height), range(self._width)):
                if self.key(end) == 'X':
                    continue
                transitions[(self.key(start), self.key(end))] = list(self._enlist_transition(start, end))
        return transitions

    def _enlist_transition(self, start, end, prefix=''):
        if start == end:
            yield prefix
        if start[1] > end[1] and self.key((start[0], start[1] - 1)) != 'X':
            yield from self._enlist_transition((start[0], start[1] - 1), end, prefix + '<')
        if start[1] < end[1] and self.key((start[0], start[1] + 1)) != 'X':
            yield from self._enlist_transition((start[0], start[1] + 1), end, prefix + '>')
        if start[0] < end[0] and self.key((start[0] + 1, start[1])) != 'X':
            yield from self._enlist_transition((start[0] + 1, start[1]), end, prefix + 'v')
        if start[0] > end[0] and self.key((start[0] - 1, start[1])) != 'X':
            yield from self._enlist_transition((start[0] - 1, start[1]), end, prefix + '^')

    def key(self, pos):
        return self._keys[pos[0]][pos[1]]

    def execute(self, code, x, y):
        n = ''
        for c in code:
            if c == 'A':
                n += self._keys[x][y]
            elif c == '<':
                y -= 1
            elif c == '>':
                y += 1
            elif c == '^':
                x -= 1
            elif c == 'v':
                x += 1
        return n

    def enumerate_sequences(self, code, current=None, prefix=''):
        if current is None:
            current = 'A'
        if len(code) == 0:
            yield prefix
            return
        for s in self._transitions[(current, code[0])]:
            yield from self.enumerate_sequences(code[1:], code[0], prefix + s + 'A')

    def shortest_segment(self, segment, level):
        if segment == '':
            return 0
        if segment == 'A':
            return 1
        if level == 0:
            return len(segment)
        if (segment, level) in self._cache:
            return self._cache[(segment, level)]
        length = min(self.shortest_sequence(p, level - 1) for p in self.enumerate_sequences(segment))
        self._cache[(segment, level)] = length
        return length

    def shortest_sequence(self, code, level):
        length = 0
        pos = 0
        while (a := code.find('A', pos)) >= 0:
            segment = code[pos:a+1]
            segment_length = self.shortest_segment(segment, level)
            length += segment_length
            pos = a + 1
        return length

    def fill_cache(self, level):
        for i in range(self._filled + 1, level + 1):
            for (k, v) in self._transitions.items():
                for p in v:
                    self.shortest_sequence(p, level)
        self._filled = level + 1


class KeypadSystem:
    def __init__(self):
        self._numeric = Keypad(['789', '456', '123', 'X0A'])
        self._directional = Keypad(['X^A', '<v>'])

    def shortest_control_sequence(self, code, level=2):
        self._directional.fill_cache(level)
        return min(self._directional.shortest_sequence(p, level) for p in self._numeric.enumerate_sequences(code))

    def complexity(self, code, level=2):
        a = int(code[:-1])
        b = self.shortest_control_sequence(code, level)
        #print(a, '*', b, '=', a * b)
        return a * b

    def total_complexity(self, codes, level=2):
        return sum(self.complexity(code, level) for code in codes)


system = KeypadSystem()

codes = load_input('input.txt')
#codes = load_input('test.txt')


print('AOC 2024 21 part 1')
print(system.total_complexity(codes))

print()

print('AOC 2024 21 part 2')
print(system.total_complexity(codes, 25))




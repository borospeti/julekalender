#!/usr/bin/env python3

import tokenize

class Calculator:
    def __init__(self):
        self.tokens = None
        self.stack = []

    def load(self, filename):
        with open(filename, 'rb') as f:
            self.tokens = list(tokenize.tokenize(f.readline))

    def push(self, data):
        self.stack.append(data)

    def pop(self):
        return self.stack.pop()

    def peek(self, depth=1):
        return self.stack[-depth] if len(self.stack) >= depth else None

    def compute(self, left, op, right):
        if op == '+':
            return left + right
        elif op == '*':
            return left * right
        else:
            raise Exception(f'invalid operator {op}')

    def evaluate(self):
        for token in self.tokens:
            if token.type == tokenize.NUMBER:
                num = int(token.string)
                if self.peek() in ['+', '*']:
                    op = self.pop()
                    left = self.pop()
                    self.push(self.compute(left, op, num))
                else:
                    self.push(num)
            elif token.type == tokenize.OP:
                if token.string == ')':
                    right = self.pop()
                    if self.pop() != '(':
                        raise Exception('syntax error', token)
                    if self.peek() in ['+', '*']:
                        op = self.pop()
                        left = self.pop()
                        self.push(self.compute(left, op, right))
                    else:
                        self.push(right)
                else:
                    self.push(token.string)
            elif token.type == tokenize.NEWLINE:
                while self.stack:
                    yield self.pop()


calculator = Calculator()
calculator.load('input.txt')
#calculator.load('mini.txt')
print(sum(calculator.evaluate()))

#!/usr/bin/env python3

import operator

from ptk.lexer import ReLexer, token
from ptk.parser import LRParser, leftAssoc, leftAssoc, production, ParseError

# normal:
# @leftAssoc('+')
# @leftAssoc('*')

# Elf basic:
# @leftAssoc('*', '+')

# Elf advanced:
# @leftAssoc('*')
# @leftAssoc('+')

@leftAssoc('*')
@leftAssoc('+')
class ElfCalc(LRParser, ReLexer):
    def newSentence(self, result):
        return result

    # Lexer
    def ignore(self, char):
        return char in [' ', '\t']

    @token(r'[1-9][0-9]*')
    def number(self, tok):
        tok.value = int(tok.value)

    # Parser
    @production('E -> "(" E<value> ")"')
    def paren(self, value):
        return value

    @production('E -> number<number>')
    def litteral(self, number):
        return number

    @production('E -> E<left> "+"<op> E<right>')
    @production('E -> E<left> "*"<op> E<right>')
    def binaryop(self, left, op, right):
        #print('Binary operation: %s %s %s' % (left, op, right))
        return {
            '+': operator.add,
            '*': operator.mul,
            }[op](left, right)


parser = ElfCalc()
with open('input.txt') as f:
    total = 0
    for line in f.readlines():
        res = parser.parse(line.strip())
        total += res
print(total)

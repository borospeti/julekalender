#!/usr/bin/env python3

START = '925176834'
TEST  = '389125467'

class CrabCups:
    def __init__(self, start):
        self.cups = start

    def pred(self, c):
        return chr(ord(c) - 1) if c > '1' else '9'

    def turn(self):
        pick = self.cups[1:4]
        dest = self.pred(self.cups[0])
        while dest in pick:
            dest = self.pred(dest)
        pos = self.cups.index(dest) + 1
        next_cups = self.cups[4:pos] + pick + self.cups[pos:] + self.cups[0]
        self.cups = next_cups

    def play(self, n):
        for i in range(n):
            self.turn()
            #print(self.cups)

    def result(self):
        pos = self.cups.index('1')
        return self.cups[pos + 1:] + self.cups[:pos]

#game = CrabCups(TEST)
game = CrabCups(START)
game.play(100)
print(game.result())


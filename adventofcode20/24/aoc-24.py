#!/usr/bin/env python3

from collections import defaultdict




class Game:
    E  = '1'
    SE = '2'
    SW = '3'
    W  = '4'
    NW = '5'
    NE = '6'

    def __init__(self):
        self.blacks = set()

    def load(self, filename):
        flip = defaultdict(int)
        with open(filename) as f:
            for line in f.readlines():
                line = (line.replace('se', self.SE).replace('sw', self.SW)
                        .replace('nw', self.NW).replace('ne', self.NE)
                        .replace('e', self.E).replace('w', self.W))
                n = (line.count(self.NE) + line.count(self.NW)) - (line.count(self.SE) + line.count(self.SW))
                e = (2 * (line.count(self.E) - line.count(self.W))
                     + (line.count(self.NE) + line.count(self.SE)) - (line.count(self.NW) + line.count(self.SW)))
                coords = (n, e)
                if coords in self.blacks:
                    self.blacks.remove(coords)
                else:
                    self.blacks.add(coords)

    def count_blacks(self):
        return len(self.blacks)

    def neighbours(self, coords):
        n, e = coords
        return { (n, e+2), (n-1, e+1), (n-1, e-1), (n, e-2), (n+1, e-1), (n+1, e+1) }

    def white_neighbours(self, coords):
        return self.neighbours(coords) - self.blacks

    def black_neighbours(self, coords):
        return self.neighbours(coords) & self.blacks

    def turn(self):
        whites = set()
        for b in self.blacks:
            whites |= self.white_neighbours(b)
        new_blacks = set()
        for b in self.blacks:
            if 1 <= len(self.black_neighbours(b)) <= 2:
                new_blacks.add(b)
        for w in whites:
            if len(self.black_neighbours(w)) == 2:
                new_blacks.add(w)
        self.blacks = new_blacks

    def play(self, n=1):
        for i in range(n):
            self.turn()


game = Game()
#game.load('mini.txt')
game.load('input.txt')

print('part 1')
print(game.count_blacks())

game.play(100)

print('part 2')
print(game.count_blacks())

#!/usr/bin/env python3

from collections import defaultdict

class Game:
    STARTING = [18, 11, 9, 0, 5, 1]

    def __init__(self):
        self.turn = 0
        self.last = None
        self.spoken = defaultdict(int)

    def take_turn(self):
        if self.turn < len(self.STARTING):
            spoken = self.STARTING[self.turn]
        elif self.spoken[self.last] == 0:
            spoken = 0
        else:
            spoken = self.turn - self.spoken[self.last]
        self.spoken[self.last] = self.turn
        self.turn += 1
        self.last = spoken

    def run(self, turns):
        for i in range(turns):
            self.take_turn()
        return self.last


print('part 1')
game = Game()
print(game.run(2020))

print('part 2')
game = Game()
print(game.run(30000000))




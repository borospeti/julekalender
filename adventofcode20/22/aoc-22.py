#!/usr/bin/env python3

from collections import deque

class Combat:
    def __init__(self):
        self.players = []

    def load_decks(self, filename):
        with open(filename) as f:
            for line in f.read().replace('\n', ' ').split('  '):
                self.players.append(deque(map(int, line.split()[2:])))

    def play_round(self):
        cards = [deck.popleft() for deck in self.players]
        winner = cards.index(max(cards))
        self.players[winner].extend(sorted(cards, reverse=True))
        return 0 not in [len(player) for player in self.players]

    def score(self):
        return [sum([a * b for a, b in zip(player, range(len(player), 0, -1))]) for player in self.players]

    def play(self):
        while self.play_round():
            pass
        return self.score()


class RecursiveCombat:
    def __init__(self, decks=None):
        self.players = []
        self.played_signatures = set()
        if decks is not None:
            for d in decks:
                self.players.append(deque(d))

    def load_decks(self, filename):
        with open(filename) as f:
            for line in f.read().replace('\n', ' ').split('  '):
                self.players.append(deque(map(int, line.split()[2:])))

    def signature(self):
        return ':'.join([','.join([str(c) for c in player]) for player in self.players])

    def play_round(self):
        sig = self.signature()
        if sig in self.played_signatures:
            return 0  # player 1 wins
        self.played_signatures.add(sig)
        cards = [deck.popleft() for deck in self.players]
        recurse = True
        for i, c in enumerate(cards):
            if c > len(self.players[i]):
                recurse = False
                break
        if recurse:
            # Recursive round
            #print('Recurse')
            recursive_game = RecursiveCombat([list(self.players[i])[:c] for i, c in enumerate(cards)])
            winner = recursive_game.play()
        else:
            # Normal round
            winner = cards.index(max(cards))
        self.players[winner].append(cards[winner])
        self.players[winner].extend(sorted(cards[:winner] + cards[winner + 1:], reverse=True))
        decks = [len(player) for player in self.players]
        if 0 in decks:
            return decks.index(max(decks))
        return None

    def score(self):
        return [sum([a * b for a, b in zip(player, range(len(player), 0, -1))]) for player in self.players]

    def play(self):
        while True:
            #print(self.players)
            winner = self.play_round()
            if winner is not None:
                #print('Winner:', winner)
                return winner


part = 2

if part == 1:
    game = Combat()
    game.load_decks('mini.txt')
    print(game.play())

    game = Combat()
    game.load_decks('input.txt')
    print('part 1')
    print(game.play())

elif part == 2:
    game = RecursiveCombat()
    game.load_decks('mini.txt')
    print(game.play())
    print(game.score())

    game = RecursiveCombat()
    game.load_decks('input.txt')
    print('part 2')
    print(game.play())
    print(game.score())



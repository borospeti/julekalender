#!/usr/bin/env python3

NISSER = 127

with open('godteri.txt') as f:
    godteri = 0
    for g in f.read().split(','):
        godteri += int(g)
        if godteri % NISSER == 0:
            print(godteri / NISSER)


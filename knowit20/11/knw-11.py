#!/usr/bin/env python3

from collections import defaultdict


PASSWORD = 'eamqia'


with open('hint.txt') as f:
    words = [line.strip() for line in f.readlines()]


def rot(word, offset=1):
    return ''.join([chr(ord('a') + (ord(c) - ord('a') + offset) % 26) for c in word])

def add(word1, word2):
    return ''.join([chr(ord('a') + (ord(x) + ord(y) - 2 * ord('a')) % 26) for x, y in zip(word1, word2)])

def gen_next(word):
    return add(word, rot(word[1:]))

def gen_passwords(word):
    l = []
    while word:
        l.append(word)
        word = gen_next(word)
    return [''.join([pwd[i] for pwd in l[:len(l) - i]]) for i in range(len(l))]

def check_hint(word, password):
    for p in gen_passwords(word):
        if password in p:
            return True
    return False

for word in words:
    if check_hint(word, PASSWORD):
        print(word)




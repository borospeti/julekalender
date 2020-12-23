#!/usr/bin/env python3

import re
from collections import defaultdict

base_words = defaultdict(int)

with open('basewords.txt') as f:
    for line in f.readlines():
        word, score = line.split()
        base_words[word] = int(score)

rap_lines = []

with open('rap_battle.txt') as f:
    for line in f.readlines():
        artist, text = line.split(':')
        rap_lines.append((artist, text.split()))

scores = defaultdict(int)

def vocal_bonus(prev_word, word):
    if prev_word is None:
        return 0
    diff = max(0, len(re.findall(r'[aeiouyæøå]', word)) - len(re.findall(r'[aeiouyæøå]', prev_word)))
    return diff

def score(artist, text):
    global scores
    prev_word = None
    prev_base = None
    rep_count = 1
    for word in text:
        if word.startswith('jule'):
            base = word[4:]
            vocal_multiplier = 2
        else:
            base = word
            vocal_multiplier = 1
        base_score = base_words[base]
        vocal_score = vocal_multiplier * vocal_bonus(prev_word, word)
        if base == prev_base:
            rep_count += 1
        else:
            rep_count = 1
        value = (base_score + vocal_score) // rep_count
        scores[artist] += value
        prev_word = word
        prev_base = base

for artist, text in rap_lines:
    score(artist, text)

print(scores)



#!/usr/bin/env python3

with open('wordlist.txt') as f:
    words = [line.strip() for line in f.readlines()]


def is_palindrome(word):
    return word == word[::-1]

def is_almost_palindrome(word):
    if len(word) < 3:
        return False
    i = 0
    while i < (len(word) - 1) // 2:
        if word[i] == word[-i-1]:
            i += 1
            continue
        if word[i] == word[-i-2] and word[i+1] == word[-i-1]:
            i += 2
            continue
        return False
    return True

aps = [word for word in words if is_almost_palindrome(word) and not is_palindrome(word)]
print(aps)
print(len(aps))


#!/usr/bin/env python3

with open('forest.txt') as f:
    lines = [l.rstrip('\n') for l in f.readlines()]

def check_tree(t):
    if not t:
        return 0
    for c in range(len(t) // 2):
        if t[c] != t[len(t) - c - 1]:
            return 0
    return 1

symm = 0
tree = []
for i in range(len(lines[0])):
    col = ''.join([l[i] for l in lines])
    if col.strip() == '':
        symm += check_tree(tree)
        tree = []
        continue
    tree.append(col)
symm += check_tree(tree)
print(symm)


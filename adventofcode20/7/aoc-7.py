#!/usr/bin/env python3

import re
import sys
import networkx as nx

bags = nx.DiGraph()
with open('input.txt') as f:
    for line in f.readlines():
        m = re.fullmatch(r'(\w+ \w+) bags? contain (\d+ \w+ \w+ bags?(?:, \d+ \w+ \w+ bags?)*)\.\s*', line)
        if m:
            colour = m.group(1)
            bags.add_node(colour)
            for content in m.group(2).split(', '):
                mm = re.fullmatch(r'(\d+) (\w+ \w+) bags?', content)
                bags.add_node(mm.group(2))
                bags.add_edge(mm.group(2), colour, amount=int(mm.group(1)))
            continue
        m = re.fullmatch(r'(\w+ \w+) bags? contain no other bags?.\s*', line)
        if not m:
            print(f'invalid line: {line.strip()}')
            sys.exit(1)
        bags.add_node(m.group(1))

print('part 1')
path = nx.single_source_shortest_path(bags, 'shiny gold')
print(len(path) - 1)

print('part 2')
def content(G, x):
    cnt = 0
    for k, v in G[x].items():
        cnt += v['amount'] * (1 + content(G, k))
    return cnt

rbags = bags.reverse()
print(content(rbags, 'shiny gold'))

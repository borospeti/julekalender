#!/usr/bin/env python3

import networkx as nx

CEO = 'Julenissen'

G = nx.DiGraph()
valid = {CEO}

#with open('mini.txt') as f:
with open('elves.txt') as f:
    for line in f.readlines():
        elves = list(map(str.strip, line.split('🎄')))
        boss = CEO
        for elf in elves:
            G.add_edge(boss, elf)
            boss = elf
        valid.add(boss)

invalid = set(G.nodes) - valid

# Der mellomledere mangler fra listen blir den manglende mellomlederen
# sine undersåtter lagt under nærmeste eksisterende mellomleder
# oppover i treet.

for elf in invalid:
    bosses = [e[0] for e in G.in_edges(elf)]
    minions = [e[1] for e in G.out_edges(elf)]
    for b in bosses:
        for m in minions:
            G.add_edge(b, m)
    G.remove_node(elf)

# Alle mellomledere med kun én direkte undersått som også er
# mellomleder får sparken. Undersåtten blir så flyttet opp ett hakk i
# organisasjonen.
for elf in list(G.nodes):
    minions = [e[1] for e in G.out_edges(elf)]
    if len(minions) == 1 and G.out_degree(minions[0]) > 0:
        bosses = [e[0] for e in G.in_edges(elf)]
        for b in bosses:
            G.add_edge(b, minions[0])
        G.remove_node(elf)


workers = len([node for node in G.nodes if G.out_degree(node) == 0])
bosses = len(G) - workers - 1
print(f'{workers} - {bosses} = {workers - bosses}')

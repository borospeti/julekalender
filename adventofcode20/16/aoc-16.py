#!/usr/bin/env python3

import networkx as nx


class Constraints:
    def __init__(self):
        self.constraints = []

    def add(self, field, ranges):
        self.constraints.append((field, [list(map(int, r.split('-'))) for r in ranges.split(' or ')]))

    def check(self, value):
        for c in self.constraints:
            for r in c[1]:
                if r[0] <= value <= r[1]:
                    return True
        return False

    def satisfies(self, value):
        fields = set()
        for c in self.constraints:
            for r in c[1]:
                if r[0] <= value <= r[1]:
                    fields.add(c[0])
                    break
        return fields

    def satisfies_all(self, values):
        sat = []
        for value in values:
            s = self.satisfies(value)
            if not s:
                return None
            sat.append(s)
        return sat

constraints = Constraints()
with open('input.txt') as f:
    while True:
        line = f.readline().strip()
        if not line:
            break
        constraints.add(*line.split(': '))
    f.readline()
    own_ticket = list(map(int, f.readline().strip().split(',')))
    f.readline()
    f.readline()
    nearby_tickets =[]
    while True:
        line = f.readline().strip()
        if not line:
            break
        nearby_tickets.append(list(map(int, line.split(','))))

print('part 1')
error = 0
for t in nearby_tickets:
    for f in t:
        if not constraints.check(f):
            error += f
print(error)

print('part 2')
sats = []
for t in nearby_tickets:
    sat = constraints.satisfies_all(t)
    if sat:
        sats.append(sat)

G = nx.Graph()
for i in range(len(sat[0])):
    for v in set.intersection(*[sat[i] for sat in sats]):
        G.add_edge(i, v)

matching = nx.algorithms.bipartite.matching.maximum_matching(G)

res = 1
for k,v in matching.items():
    if isinstance(k, str) and k[:9] == 'departure':
       res *= own_ticket[v]
print(res)

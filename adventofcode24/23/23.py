#!/usr/bin/env python3

import networkx as nx


def load_input(filename):
    network = {}
    graph = nx.Graph()
    with open(filename) as f:
        for line in f:
            (a, b) = line.strip().split('-')
            if not a in network:
                network[a] = set()
            if not b in network:
                network[b] = set()
            network[a].add(b)
            network[b].add(a)
            graph.add_edge(a, b)
    return (network, graph)


def find_triplets(network, filter_t=True):
    for a in network.keys():
        if filter_t and not a.startswith('t'):
            continue
        for b in network[a]:
            cs = network[a].intersection(network[b])
            cs.discard(a)
            for c in cs:
                yield '-'.join(sorted((a, b, c)))


def maximum_clique(network):
    for node in network.keys():
        for excluded in network[node]:
            testing = network[node].difference({excluded})
            clique = testing.union({node})
            size = len(clique)
            for neighbour in testing:
                clique.intersection_update(network[neighbour].union({neighbour}))
                if len(clique) < size:
                    break
            if len(clique) == size:
                return size, ','.join(sorted(clique))


(network, graph) = load_input('input.txt')
#(network, graph) = load_input('test.txt')

triplets = set(find_triplets(network))
#for t in triplets:
#    print(t)

(size, password) = maximum_clique(network)

#party = nx.approximation.max_clique(graph)
#size = len(party)
#password = ','.join(sorted(party))


print('AOC 2024 23 part 1')
print(len(triplets))

print()

print('AOC 2024 23 part 2')
print(size, password)

# apx: "cx,fr,gw,is,jk,nb,nn,ns,nx,uo,we,ys"
# max: "ch,cz,di,gb,ht,ku,lu,tw,vf,vt,wo,xz,zk"



#!/usr/bin/env python3

import networkx as nx
import re
from queue import deque


styles = { 'AND': 'red', 'OR': 'blue', 'XOR': 'green' }


def load_input(filename):
    network = nx.DiGraph()
    seed = deque()
    with open(filename) as f:
        while line := f.readline().strip():
            node, value = line.split(':')
            network.add_node(node, value=int(value))
            seed.append(node)
        while line := f.readline().strip():
            m = re.match(r'^(\w+) (AND|OR|XOR) (\w+) -> (\w+)$', line)
            network.add_node(m.group(4), value=None, op=m.group(2), style="filled", fillcolor=styles[m.group(2)])
            network.add_edge(m.group(1), m.group(4))
            network.add_edge(m.group(3), m.group(4))
    return (network, seed)


def evaluate(network, seed):
    while len(seed) > 0:
        a = seed.popleft()
        v = network.nodes[a]['value']
        for b in network.successors(a):
            if network.nodes[b]['value'] is None:
                network.nodes[b]['value'] = v
            else:
                if network.nodes[b]['op'] == 'AND':
                    network.nodes[b]['value'] &= v
                elif network.nodes[b]['op'] == 'OR':
                    network.nodes[b]['value'] |= v
                elif network.nodes[b]['op'] == 'XOR':
                    network.nodes[b]['value'] ^= v
                seed.append(b)
    zz = [network.nodes[z2]['value'] for z2 in sorted([z1 for z1 in network.nodes if z1.startswith('z')], reverse=True)]
    z = 0
    for bit in zz:
        z = (z << 1) + bit
    return z


def print_network(network, filename):
    agraph = nx.nx_agraph.to_agraph(network)
    agraph.draw(filename, prog="neato")


network, seed = load_input('input.txt')

#print(list(network.nodes(data=True)))

z = evaluate(network, seed)

print_network(network, "adder.png")


print('AOC 2024 24 part 1')
print(z)

print()

print('AOC 2024 24 part 2')
print("bhd,brk,dhg,dpd,nbf,z06,z23,z38")

# dhg - z06
# dpd - brk
# z23 - bhd
# nbf - z38





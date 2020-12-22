#!/usr/bin/env python3

import re
from collections import namedtuple, defaultdict
import networkx as nx

Food = namedtuple('Food',['index', 'ingredients','allergens'])

foods = []
#with open('mini.txt') as f:
with open('input.txt') as f:
    for line in f.readlines():
        m = re.fullmatch(r'\s*(\w+(?:\s+\w+)*)\s+\(contains\s+(\w+(?:[ ,]+\w+)*)\)\s*', line)
        if m:
            foods.append(Food(len(foods), m.group(1).split(), re.split(r'[ ,]+', m.group(2))))


allergen_map = {}
ingredient_map = defaultdict(list)
for food in foods:
    for a in food.allergens:
        if a not in allergen_map:
            allergen_map[a] = set(food.ingredients)
        else:
            allergen_map[a].intersection_update(set(food.ingredients))
    for i in food.ingredients:
        ingredient_map[i].append(food.index)
possible_allergens = set.union(*allergen_map.values())
#print(allergen_map)
#print(possible_allergy)
count = 0
for i, f in ingredient_map.items():
    if i not in possible_allergens:
        count += len(f)

print('part 1')
print(count)

G = nx.Graph()
for a, ingredients in allergen_map.items():
    for i in ingredients:
        G.add_edge(a, i)
matching = nx.algorithms.bipartite.matching.maximum_matching(G)
print(matching)
print('part 2')
print(','.join([matching[k] for k in sorted(matching) if k in allergen_map]))



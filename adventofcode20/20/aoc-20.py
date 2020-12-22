#!/usr/bin/env python3

from collections import defaultdict
import networkx as nx


tiles = {}
edge_map = defaultdict(list)

def reverse_bits(n):
    return int(f'{n:010b}'[::-1], 2)

class Tile:
    def __init__(self, tile_id, bitmap):
        self.tile_id = tile_id
        self.bitmap = bitmap
        # top, right, bottom, left
        self.edges = [int(bitmap[0], 2),
                      int(''.join([row[-1] for row in bitmap]), 2),
                      int(bitmap[-1][::-1], 2),
                      int(''.join([row[0] for row in bitmap[::-1]]), 2)]
        for edge in self.edges:
            edge_map[edge].append(self.tile_id)


with open('input.txt') as f:
#with open('mini.txt') as f:
    trans = str.maketrans('.#', '01')
    tid = None
    tile = []
    for line in map(str.strip, f.readlines()):
        if line[:4] == 'Tile':
            if tid is not None:
                tiles[tid] = Tile(tid, tile)
            tid = int(line[5:-1])
            tile = []
        elif line:
            tile.append(line.translate(trans))
    if tid is not None:
        tiles[tid] = Tile(tid, tile)

    match_count = {} #defaultdict(int)
    for tile in tiles.values():
        match_count[tile.tile_id] = 0
        for edge in tile.edges:
            #for match in set(edge_map[reverse(edge)]) - {tile.tile_id}:
            #    print(tile.tile_id, match)
            #    G.add_edge(tile.tile_id, match)
            #print(set(edge_map[reverse(edge)]) - {tile.tile_id})
            if (set(edge_map[reverse_bits(edge)]) | set(edge_map[edge])) - {tile.tile_id}:
                match_count[tile.tile_id] += 1
    corners = 1
    for k, v in match_count.items():
        #print(v, k)
        if v == 2:
            corners *= k
    print(corners)


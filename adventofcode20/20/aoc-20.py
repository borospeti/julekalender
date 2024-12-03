#!/usr/bin/env python3

from collections import defaultdict
from math import prod
import networkx as nx


class Tile:
    TOP    = 0
    RIGHT  = 1
    BOTTOM = 2
    LEFT   = 3
    def __init__(self, tile_id, bitmap):
        self.tile_id = tile_id
        self.bitmap = bitmap
        # 0:top, 1:right, 2:bottom, 3:left
        self.edges = [int(''.join(bitmap[0]), 2),
                      int(''.join([row[-1] for row in bitmap]), 2),
                      int(''.join(bitmap[-1][::-1]), 2),
                      int(''.join([row[0] for row in bitmap[::-1]]), 2)]
        self.rotation = 0
        self.mirror = False
        self.transformed = None

    @staticmethod
    def reverse_bits(n):
        return int(f'{n:010b}'[::-1], 2)

    def register_edges(self, edge_map):
        for edge in self.edges:
            edge_map[edge].append(self.tile_id)

    def transform(self, rotation, mirror=False):
        self.rotation = rotation
        self.mirror = mirror
        if self.rotation == 0:
            self.transformed = self.bitmap
        elif self.rotation == 1:
            self.transformed = [[self.bitmap[i][j] for i in range(9, -1, -1)] for j in range(10)]
        elif self.rotation == 2:
            self.transformed = [row[::-1] for row in self.bitmap[::-1]]
        elif self.rotation == 3:
            self.transformed = [[self.bitmap[i][j] for i in range(10)] for j in range(9, -1, -1)]
        if self.mirror:
            self.transformed = [row[::-1] for row in self.transformed]

    def transformed_edge(self, edge_idx, rot=None, mirr=None):
        if rot is None:
            rot = self.rotation
        if mirr is None:
            mirr = self.mirror
        if not mirr:
            return self.edges[(edge_idx - rot) % 4]
        offset = edge_idx - rot
        if edge_idx % 2 == 1:
            offset += 2
        return self.reverse_bits(self.edges[offset % 4])

    def top_edge(self):
        return self.transformed_edge(self.TOP)

    def right_edge(self):
        return self.transformed_edge(self.RIGHT)

    def bottom_edge(self):
        return self.transformed_edge(self.BOTTOM)

    def left_edge(self):
        return self.transformed_edge(self.LEFT)

    def find_matching_edge(self, edge, edge_idx=0):
        rev_edge = self.reverse_bits(edge)
        for mirr in [False, True]:
            for rot in range(4):
                if self.transformed_edge(edge_idx, rot, mirr) == rev_edge:
                    return (rot, mirr)
        return None

    def get_pixel(self, i, j):
        return self.transformed[i+1][j+1]

    def put_pixel(self, pixel, i, j):
        self.transformed[i+1][j+1] = pixel

    def __repr__(self):
        return f'Tile {self.tile_id} (r:{self.rotation} m:{self.mirror})'


class Picture:
    TRANS = str.maketrans('.#', '01')
    MONSTER = ['                  # ',
               '#    ##    ##    ###',
               ' #  #  #  #  #  #   ']
    def __init__(self):
        self.tiles = {}
        self.edge_map = defaultdict(list)
        self.corners = []
        self.grid = []
        self.monster = [(i, j) for i in range(len(self.MONSTER)) for j in range(len(self.MONSTER[i]))
                        if self.MONSTER[i][j] == '#']
        self.monster_h = len(self.MONSTER)
        self.monster_w = len(self.MONSTER[0])
        self.h = None
        self.w = None

    def load(self, filename):
        with open(filename) as f:
            tid = None
            tile = []
            for line in map(str.strip, f.readlines()):
                if line[:4] == 'Tile':
                    if tid is not None:
                        self.tiles[tid] = Tile(tid, tile)
                    tid = int(line[5:-1])
                    tile = []
                elif line:
                    tile.append(list(line.translate(self.TRANS)))
            if tid is not None:
                self.tiles[tid] = Tile(tid, tile)
        for tile in self.tiles.values():
            tile.register_edges(self.edge_map)

    def matching_tiles_for_edge(self, tile, edge):
        return (set(self.edge_map[Tile.reverse_bits(edge)]) | set(self.edge_map[edge])) - {tile.tile_id}

    def matching_tiles(self, tile):
        return [self.matching_tiles_for_edge(tile, edge) for edge in tile.edges]

    def matching_tile_and_trans(self, tile, edge_idx):
        edge = tile.transformed_edge(edge_idx)
        matching = list(self.matching_tiles_for_edge(tile, edge))
        if len(matching) == 1:
            next_tile = self.tiles[matching[0]]
            next_trans = next_tile.find_matching_edge(edge, (edge_idx + 2) % 4)
            return next_tile, next_trans
        elif len(matching) > 1:
            raise Exception('too many matching tiles')
        return None, None

    def find_corners(self):
        self.corners = []
        for tile in self.tiles.values():
            if sum([1 for m in self.matching_tiles(tile) if m]) == 2:
                self.corners.append(tile.tile_id)

    def build(self):
        self.grid = []
        # 1. pick top left corner
        corner = self.tiles[self.corners[0]]
        #corner = self.tiles[1951] ############################ HACK
        matching = self.matching_tiles(corner)
        if not (matching[3] | matching[0]):
            rotation = 0
        elif not (matching[0] | matching[1]):
            rotation = 3
        elif not (matching[1] | matching[2]):
            rotation = 2
        elif not (matching[2] | matching[3]):
            rotation = 1
        else:
            raise Exception(f'Corner problem: {matching}')
        corner.transform(rotation, False)
        tile = corner
        while tile is not None:
            row = [tile]
            self.grid.append(row)
            while True:
                tile, trans = self.matching_tile_and_trans(tile, Tile.RIGHT)
                if tile is None:
                    break
                tile.transform(*trans)
                row.append(tile)
            tile, trans = self.matching_tile_and_trans(row[0], Tile.BOTTOM)
            if tile is not None:
                tile.transform(*trans)
        self.h = 8 * len(self.grid)
        self.w = 8 * len(self.grid[0])

    def coord_trans(self, i, j, rot, mirr):
        if rot == 1:
            i, j = j, -i
        elif rot == 2:
            i, j = -i, -j
        elif rot == 3:
            i, j = -j, i
        if mirr:
            j = -j
        i %= 8 * len(self.grid)
        j %= 8 * len(self.grid[0])
        return i, j

    def get_pixel(self, i, j, rot=0, mirr=False):
        i, j = self.coord_trans(i, j, rot, mirr)
        return self.grid[i >> 3][j >> 3].get_pixel(i & 7, j & 7)

    def put_pixel(self, pixel, i, j, rot=0, mirr=False):
        i, j = self.coord_trans(i, j, rot, mirr)
        self.grid[i >> 3][j >> 3].put_pixel(pixel, i & 7, j & 7)

    def check_monster(self, i, j, rot, mirr):
        for m in self.monster:
            if self.get_pixel(i + m[0], j + m[1], rot, mirr) == '0':
                return False
        return True

    def mark_monster(self, i, j, rot, mirr):
        for m in self.monster:
            self.put_pixel('2', i + m[0], j + m[1], rot, mirr)

    def find_monsters(self):
        for rot in range(4):
            for mirr in (True, False):
                for i in range(self.h - self.monster_h + 1):
                    for j in range(self.h - self.monster_h + 1):
                        if self.check_monster(i, j, rot, mirr):
                            self.mark_monster(i, j, rot, mirr)
        water = 0
        for i in range(self.h):
            for j in range(self.w):
                if self.get_pixel(i, j) == '1':
                    water += 1
        return water


picture = Picture()
picture.load('input.txt')
#picture.load('mini.txt')
print('part 1')
picture.find_corners()
print(prod(picture.corners))

print('part 2')
picture.build()
#print(picture.grid)
print(picture.find_monsters())
#for i in range(24):
#    for j in range(24):
#        print(f'{picture.get_pixel(i, j)} ', end='')
#    print()

import logging
from collections import namedtuple

DIRECTIONS = ['U', 'R', 'D', 'L']

Side = namedtuple('Side', ['tile', 'direction', 'flipped', 'side'])


class Tile:
    tileId = None
    tile = None
    rotation = None
    flipped = None

    def __init__(self, tile):
        tile_id = tile[0][5:-1]
        self.tileId = int(tile_id)
        self.tile = tile[1:].copy()
        self.flipped = False
        self.rotation = 0

    def get_all_sides(self):
        tile = self.tile
        up = tile[0]
        down = tile[-1][::-1]
        left = []
        right = []
        for line in tile:
            left.append(line[0])
            right.append(line[-1])
        right = ''.join(right)
        left = ''.join(left)[::-1]
        sides = sorted([Side(self.tileId, (i + self.rotation) % 4, self.flipped, side) for (i, side) in
                        enumerate([up, right, down, left])])
        sidesRev = sorted([Side(self.tileId, (i + self.rotation) % 4, not self.flipped, side[::-1]) for (i, side) in
                           enumerate([down, right, up, left])])
        self.sides = sides + sidesRev
        return self.sides

    def flip(self, flipVal):
        self.flipped = flipVal

    def rotate(self, angle):
        self.rotation = angle

    def get_side(self, direction):
        sides = self.get_all_sides()
        if self.flipped:
            return sides[(direction) % 4 + 4]
        else:
            return sides[(direction) % 4]

    def flip_text(self, text):
        return text[::-1]

    def rotate_text(self, text):
        return [''.join(elem) for elem in zip(*text[::-1])]

    def display_full(self):
        tmp_txt = self.tile
        if self.flipped:
            tmp_txt = self.flip_text(tmp_txt)
        for i in range(self.rotation):
            tmp_txt = self.rotate_text(tmp_txt)
        return tmp_txt

    def display_no_border(self):
        txt = self.display_full()
        return [line[1:-1] for line in txt[1:-1]]


class TileList:
    tiles = None
    all_sides = None

    def __init__(self):
        self.tiles = {}
        self.all_sides = {}

    def add_tile(self, tile):
        self.tiles[tile.tileId] = tile
        for side in tile.get_all_sides():
            if side.side in self.all_sides:
                self.all_sides[side.side].append(side)
            else:
                self.all_sides[side.side] = [side]

    def find_neigh_in_direction(self, tile, direction):
        s = self.tiles[tile].get_side(direction)
        logging.debug((s, dir))
        matching_side = [side for side in self.all_sides[s.side[::-1]] if side.tile != s.tile]
        logging.debug(matching_side)
        if matching_side:
            return matching_side[0]
        else:
            return None

    def find_neigh(self, start):
        visited = set()
        to_visit = []
        graph = {}
        for i in range(4):
            to_visit.append((start, i))
        while to_visit:
            (cur, dir) = to_visit.pop()
            next_side = self.find_neigh_in_direction(cur, dir)
            if next_side:
                (t, orientation, fl, _) = next_side
                graph[cur, dir] = t
                graph[t, (dir + 2) % 4] = cur
                if t not in visited:
                    rotation = [2, 3, 0, 1][(dir - orientation) % 4]
                    self.tiles[t].rotate(rotation)
                    self.tiles[t].flip(fl)
                    visited.add(t)
                    for i in range(4):
                        to_visit.append((t, i))
        logging.debug(("graph", graph))
        return graph

    def build_map(self):
        start = list(self.tiles.keys())[0]
        graph = self.find_neigh(start)

        top_left = start
        while (top_left, 0) in graph:
            top_left = graph[(top_left, 0)]
            logging.debug(top_left)

        while (top_left, 3) in graph:
            top_left = graph[(top_left, 3)]
        logging.debug(("top_left", top_left))
        cur = top_left
        lines = [cur]
        while (cur, 2) in graph:
            cur = graph[(cur, 2)]
            lines.append(cur)
        logging.debug(("lines", lines))

        map = []
        for line in lines:
            tmp = [line]
            cur = line
            while (cur, 1) in graph:
                cur = graph[(cur, 1)]
                tmp.append(cur)
            map.append(tmp)
        logging.debug(map)

        tiles_str = []
        for line in map:
            tmp = []
            for tile in line:
                print(tile)
                tmp.append(self.tiles[tile].display_no_border())
            tmp2 = [''.join(elem) for elem in zip(*tmp)]
            tiles_str += tmp2
        return tiles_str

class TextMap:
    map = None

    def __init__(self, tiles, tilelist):
        pass

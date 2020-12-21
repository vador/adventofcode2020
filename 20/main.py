import logging
import re
import cProfile
import math
from collections import namedtuple
from loadValues import LoadValues

DIRECTIONS = ['U', 'R', 'D', 'L']

Side = namedtuple('Side', ['tile', 'direction', 'flipped', 'side'])


class Tile:
    tildeId = None
    tile = None
    rotation = None
    flipped = None

    def __init__(self, tile):
        tile_id = tile[0][5:-1]
        self.tildeId = int(tile_id)
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
        sides = [Side(self.tildeId, i, False, side) for (i, side) in enumerate([up, right, down, left])]
        sidesRev = [Side(self.tildeId, i, True, side[::-1]) for (i, side) in enumerate([up, left, down, right])]
        self.sides = sides + sidesRev
        return self.sides

    def flip(self):
        self.flipped = not self.flipped

    def rotate(self, angle):
        self.rotation = angle

    def get_side(self, direction):
        if self.flipped:
            return self.sides[(direction + self.rotation) % 4 + 4]
        else:
            return self.sides[(direction + self.rotation) % 4]


class TileList:
    tiles = None
    all_sides = None

    def __init__(self):
        self.tiles = {}
        self.all_sides = {}

    def add_tile(self, tile):
        self.tiles[tile.tildeId] = tile
        for side in tile.get_all_sides():
            if side.side in self.all_sides:
                self.all_sides[side.side].append(side)
            else:
                self.all_sides[side.side] = [side]

    def find_neigh(self, tile, direction):
        pass

def main():
    number = 0

    lv = LoadValues("test.txt", groups=True)

    lst = set()
    TL = TileList()
    for tile in lv.raw_values:
        T = Tile(tile)
        TL.add_tile(T)

    logging.debug(TL.all_sides)
    tiles_uniqueside = [[s.tile for s in sides][0] for (strside, sides) in TL.all_sides.items() if len(sides) == 1]
    logging.debug(tiles_uniqueside)
    tiles_countunique = {}
    for tile in tiles_uniqueside:
        if tile in tiles_countunique:
            tiles_countunique[tile] += 1
        else:
            tiles_countunique[tile] = 1
    corners = set([tile for (tile, cnt) in tiles_countunique.items() if cnt == 4])
    logging.debug(corners)
    number = math.prod(corners)
    print("Star 1 : ", number)

    tile1 = TL.tiles[1427]
    for i in range(4):
        s1 = tile1.get_side(i)
        logging.debug(s1)
    tile1.flip()
    for i in range(4):
        s1 = tile1.get_side(i)
        logging.debug(s1)

    print("Star 2 : ", number)


##
if __name__ == '__main__':
    pr = cProfile.Profile()
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Started')
    pr.enable()

    main()
    pr.disable()

    logging.info('Finished')
    # pr.print_stats()

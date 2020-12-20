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
    direction = None
    flipped = None

    def __init__(self, tile):
        tile_id = tile[0][5:-1]
        self.tildeId = int(tile_id)
        self.tile = tile[1:].copy()

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
        sides = [Side(self.tildeId, i, False, side) for (i, side) in enumerate([up, left, down, right])]
        sidesRev = [Side(self.tildeId, i, True, side[::-1]) for (i, side) in enumerate([up, right, down, left])]
        return sides + sidesRev


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

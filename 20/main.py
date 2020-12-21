import logging
import re
import cProfile
import math
from collections import namedtuple
from loadValues import LoadValues
from tile import Tile, TileList


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

    tiles_str = TL.build_map()
    print('\n'.join(tiles_str[::-1]))

    print("Star 2 : ", number)


##
if __name__ == '__main__':
    pr = cProfile.Profile()
    logging.basicConfig(level=logging.INFO)
    logging.info('Started')
    pr.enable()

    main()
    pr.disable()

    logging.info('Finished')
    # pr.print_stats()

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

    graph = TL.find_neigh(3079)
    top_left = 3079
    logging.debug(top_left)
    while (top_left, 0) in graph:
        top_left = graph[(top_left, 0)]
        logging.debug(top_left)

    while (top_left, 3) in graph:
        top_left = graph[(top_left, 3)]
    logging.debug(top_left)
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
            tmp.append(TL.tiles[tile].display_no_border())
        tmp2 = [a + b + c for (a, b, c) in zip(*tmp)]
        tiles_str += tmp2
    print('\n'.join(tiles_str))

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

import logging
import re
import cProfile
import math

from loadValues import LoadValues


def parse_tile(tile):
    tile_id = tile[0][5:-1]
    up = tile[1]
    down = tile[-1]
    left = []
    right = []
    for line in tile[1:]:
        left.append(line[0])
        right.append(line[-1])
    return tile_id, up, ''.join(right), down[::-1], ''.join(left)[::-1]


dir = dict()
all_sides = dict()
tiles = dict()


def add_tile_to_list(tile):
    tile_id, up, right, down, left = tile
    for side in (up, right, down, left):
        if side in all_sides:
            all_sides[side].append(tile_id)
        else:
            all_sides[side] = [tile_id]
        revside = side[::-1]
        if revside in all_sides:
            all_sides[revside].append(tile_id)
        else:
            all_sides[revside] = [tile_id]


def main():
    number = 0

    lv = LoadValues("input.txt", groups=True)

    lst = set()
    for tile in lv.raw_values:
        t = parse_tile(tile)
        logging.debug(t)
        add_tile_to_list(t)
        tile_id, up, right, down, left = t

        lst |= {up, down, right, left}

    print(len(lv.raw_values))
    print(len(lst))
    print(all_sides)
    res = {}
    for side in all_sides:
        tiles = all_sides[side]
        if len(tiles) == 1:
            if tiles[0] in res:
                res[tiles[0]] += 1
            else:
                res[tiles[0]] = 1
    print([int(tile) for tile in res if res[tile] == 4])

    number = math.prod([int(tile) for tile in res if res[tile] == 4])
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

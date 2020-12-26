import logging
import re
import cProfile
from collections import namedtuple, deque
from loadValues import LoadValues
import itertools


def get_neighbours(pos):
    E_N = [(-1, -1), (-1, 0), (0, 1), (1, 0), (1, -1), (0, -1)]
    O_N = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (0, -1)]
    (x, y) = pos
    neigh = []
    if x % 2:
        for (dx, dy) in O_N:
            neigh.append((x + dx, y + dy))
    else:
        for (dx, dy) in E_N:
            neigh.append((x + dx, y + dy))
    return neigh


def game(pos_list):
    to_check = set()
    new_pos = set()
    for pos in pos_list:
        to_check |= set(get_neighbours(pos))
    for pos in to_check:
        occupied = len(pos_list & set(get_neighbours(pos)))
        if pos in pos_list and (occupied > 0 and occupied <= 2):
            new_pos.add(pos)
        else:
            if occupied == 2:
                new_pos.add(pos)
    return new_pos


def parse_directions(line):
    dirs = []
    cnt = 0
    token = ""
    for c in line:
        if c == 's' or c == 'n':
            token = c
        else:
            token += c
            dirs.append(token)
            token = ''
    return dirs


class pointer:
    pos = None
    color = None

    def __init__(self):
        self.pos = (0, 0)
        self.color = True

    def __eq__(self, other):
        return self.pos == other.pos

    def move(self, dir):
        (x, y) = self.pos

        if dir == 'e':
            y += 1
        elif dir == 'w':
            y -= 1
        else:
            d1 = dir[0]
            d2 = dir[1]

            if x % 2:
                if d2 == 'e':
                    y += 1
            else:
                if d2 == 'w':
                    y -= 1

            if d1 == 'n':
                x -= 1
            else:
                x += 1

        self.pos = (x, y)

    def __repr__(self):
        return "C: " + str(self.pos)


def main():
    number = 0

    lv = LoadValues("input.txt")
    lines = lv.strip_lines()

    print(lines[0])
    dirs = (parse_directions(lines[0]))
    c = pointer()
    for dir in dirs:
        c.move(dir)
        print(dir, c)

    tiles = {}
    for line in lines:
        dirs = parse_directions(line)
        c = pointer()
        for dir in dirs:
            c.move(dir)
        if c.pos in tiles:
            tiles.pop(c.pos)
        else:
            tiles[c.pos] = c
    print(tiles)
    number = len(tiles)

    print("Star 1 : ", number)

    new_pos = tiles.keys()
    for i in range(100):
        new_pos = game(new_pos)
        print(i + 1, len(new_pos))

    number = len(new_pos)

    print("Star 2 : ", number)


##
if __name__ == '__main__':
    pr = cProfile.Profile()
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Started')
    pr.enable()

    played_hands = {}

    main()
    pr.disable()

    logging.info('Finished')
    # pr.print_stats()

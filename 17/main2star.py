import logging
import re
import cProfile

from loadValues import LoadValues

NEIGH = []
for x in [-1, 0, 1]:
    for y in [-1, 0, 1]:
        for z in [-1, 0, 1]:
            for w in [-1, 0, 1]:
                NEIGH.append((x, y, z, w))

NEIGH = set(NEIGH)
NEIGH.discard((0, 0, 0, 0))


class Coord:
    pos = None
    NEIGH = None

    def __init__(self, pos):
        self.pos = pos
        self.NEIGH = NEIGH

    def add(self, point):
        (dx, dy, dz, dw) = point.pos
        (x, y, z, w) = self.pos
        return Coord((x + dx, y + dy, z + dz, w + dw))

    def get_neigh(self):
        neigh = set()
        for coord in self.NEIGH:
            neigh.add(self.add(Coord(coord)))
        return neigh

    def __eq__(self, other):
        return self.pos == other.pos

    def __hash__(self):
        return hash(self.pos)

    def __repr__(self):
        return "C:" + str(self.pos)


class PocketDim:
    ACTIVE = '#'
    active = None

    def __init__(self):
        self.active = set()

    def fill_pocket_dim(self, str_desc):
        (x, y, z, w) = (0, 0, 0, 0)
        for (x, line) in enumerate(str_desc):
            for (y, val) in enumerate(line):
                if val == self.ACTIVE:
                    self.active.add(Coord((x, y, z, w)))

    def step(self):
        newPD = PocketDim()
        to_search = set()
        for coord in self.active:
            to_search.update(coord.get_neigh())

        for coord in to_search:
            neigh = coord.get_neigh()
            nb = len(neigh.intersection(self.active))
            if coord in self.active and (nb == 2 or nb == 3):
                newPD.active.add(coord)
            elif nb == 3:
                newPD.active.add(coord)
        return newPD


def main():
    number = 0

    lv = LoadValues()
    grid = lv.strip_lines()
    myPD = PocketDim()
    myPD.fill_pocket_dim(grid)

    logging.debug(myPD.active)
    myP = Coord((1, 1, 1, 1))

    logging.debug(myP.get_neigh())

    for i in range(6):
        myPD = myPD.step()
        logging.debug((len(myPD.active), myPD.active))

    number = len(myPD.active)
    print("Star 1 : ", number)

    print("Star 2 : ", number)
    logging.info('Finished')


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

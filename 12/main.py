import logging
import re
import cProfile

from loadValues import LoadValues


class Ship:
    DIRECTIONS = ['E', 'N', 'W', 'S']
    pos = None
    direction = None

    def __str__(self):
        repr = "Ship: " + str(self.pos) + " : " + self.DIRECTIONS[self.direction]
        return repr

    def __init__(self):
        self.pos = (0, 0)
        self.direction = 0

    def act(self, move):
        (x, y) = self.pos
        orig_move = move
        (action, qty) = move
        qty = int(qty)
        if action == 'F':
            action = self.DIRECTIONS[self.direction]
        if action == 'E':
            x += qty
        elif action == 'W':
            x -= qty
        elif action == 'N':
            y -= qty
        elif action == 'S':
            y += qty

        if action == 'R':
            n = qty // 90
            self.direction = (self.direction - n) % 4
        elif action == 'L':
            n = qty // 90
            self.direction = (self.direction + n) % 4

        self.pos = (x, y)
        logging.debug(str(orig_move) + str(self))
        return self.pos


class ShipW:
    DIRECTIONS = ['E', 'N', 'W', 'S']
    pos = None
    wpos = None
    direction = None

    def __str__(self):
        repr = "Ship: pos " + str(self.pos) + " : waypoint : " + str(self.wpos)
        return repr

    def __init__(self):
        self.pos = (0, 0)
        self.wpos = 10, -1
        self.direction = 0

    def act(self, move):
        (x, y) = self.pos
        (wx, wy) = self.wpos
        orig_move = move
        (action, qty) = move
        qty = int(qty)
        if action == 'F':
            (x, y) = (x + wx * qty, y + wy * qty)
        if action == 'E':
            wx += qty
        elif action == 'W':
            wx -= qty
        elif action == 'N':
            wy -= qty
        elif action == 'S':
            wy += qty

        alpha = 0
        number_quarter_turn = qty // 90
        if action == 'R':
            alpha = number_quarter_turn % 4
        elif action == 'L':
            number_quarter_turn = qty // 90
            alpha = -number_quarter_turn % 4
        if alpha == 1:
            (wx, wy) = (-wy, wx)
        elif alpha == 2:
            (wx, wy) = (-wx, -wy)
        elif alpha == 3:
            (wx, wy) = (wy, -wx)

        self.pos = (x, y)
        self.wpos = (wx, wy)
        logging.debug(str(orig_move) + str(self))
        return self.pos


def main():
    lv = LoadValues()
    action_list = [(line[0], line[1:]) for line in lv.strip_lines()]
    logging.debug(action_list)
    ship = Ship()
    for action in action_list:
        pass
        ship.act(action)
    (x, y) = ship.pos
    number = abs(x) + abs(y)

    print("Star 1 : ", number)

    ship = ShipW()
    for action in action_list:
        ship.act(action)
    (x, y) = ship.pos
    number = abs(x) + abs(y)

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

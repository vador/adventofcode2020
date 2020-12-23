import logging
import re
import cProfile
from collections import namedtuple, deque
from loadValues import LoadValues
import itertools


def main():
    number = 0

    lv = LoadValues("input.txt", groups=True)

    print("Star 1 : ", number)

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

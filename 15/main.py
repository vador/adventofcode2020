import logging
import re
import cProfile

from loadValues import LoadValues


def numbers_sequence(start, end_round):
    spoken = {}
    rnd = 1
    last_spoken = 0
    for (i, val) in enumerate(start):
        spoken[val] = i + 1
        last_spoken = val
    first_time = True
    rnd = i + 2
    logging.debug(spoken)
    while rnd <= end_round:
        if last_spoken in spoken:
            last_time = spoken[last_spoken]
            spoken[last_spoken] = rnd - 1
            last_spoken = rnd - 1 - last_time
        else:
            spoken[last_spoken] = rnd - 1
            last_spoken = 0
        if (not (rnd % 1000000) or (end_round - rnd) < 30):
            logging.debug((rnd, last_spoken))

        rnd += 1
    return last_spoken


def main():
    number = 0

    lv = LoadValues()
    lines = lv.strip_lines()

    start = [0, 3, 6]
    start = [3, 1, 2]
    start = [1, 0, 18, 10, 19, 6]  # Real Input
    number = numbers_sequence(start, 2020)

    print("Star 1 : ", number)

    number = numbers_sequence(start, 30000000)

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

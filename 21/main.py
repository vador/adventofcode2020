import logging
import re
import cProfile
import math
from collections import namedtuple
from loadValues import LoadValues


def parse_recipe(line):
    ingr, aller = line[:-1].split(' (contains ')
    ingr_list = ingr.split(' ')
    aller_list = aller.split(', ')
    # logging.debug((ingr_list, aller_list))
    return ingr_list, aller_list


def main():
    number = 0

    lv = LoadValues("input.txt")
    lines = lv.strip_lines()
    possib_aller = dict()
    all_ingredients = set()
    for line in lines:
        (ingredients, allergens) = parse_recipe(line)
        all_ingredients |= set(ingredients)
        for aller in allergens:
            if aller in possib_aller:
                possib_aller[aller] &= set(ingredients)
            else:
                possib_aller[aller] = set(ingredients)

    logging.debug(possib_aller)
    # logging.debug(ingredients)
    remove_ingr = set()
    for (aller, ingr) in possib_aller.items():
        remove_ingr |= ingr

    # logging.debug(remove_ingr)
    no_aller = all_ingredients - remove_ingr
    logging.debug(no_aller)

    cnt = 0
    for line in lines:
        (ingredients, allergens) = parse_recipe(line)
        cnt += len(set(ingredients) & no_aller)

    number = cnt
    print("Star 1 : ", number)

    candidate_aller = possib_aller.copy()
    to_remove = []
    found = []
    for (aller, ingr) in candidate_aller.copy().items():
        if len(ingr) == 1:
            val = ingr.pop()
            to_remove.append(val)
            found.append((aller, val))
            candidate_aller.pop(aller)
    logging.debug(">>>>>")
    logging.debug(candidate_aller)
    logging.debug(to_remove)
    logging.debug(found)
    logging.debug(">>>>>")

    while to_remove:
        cur_ingr = to_remove.pop()
        logging.debug(cur_ingr)
        for (aller, ingr) in candidate_aller.copy().items():
            ingr.discard(cur_ingr)
            if len(ingr) == 1:
                val = ingr.pop()
                to_remove.append(val)
                found.append((aller, val))
                candidate_aller.pop(aller)
        logging.debug("-------")
        logging.debug(candidate_aller)
        logging.debug(to_remove)
        logging.debug(found)
        logging.debug("-------")

    found.sort()
    logging.debug(found)
    number = ','.join([ingr for (aller, ingr) in found])

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

import logging
import re

from loadValues import LoadValues


def is_sum(number, candidates):
    cd = set(candidates)
    res = False
    while len(cd) > 0:
        first = cd.pop()
        if number - first in cd:
            return True
    return False


def is_contiguous_ok(number, pos, list):
    acc = 0
    cur_pos = pos
    res = False
    while acc < number:
        acc += list[cur_pos]
        if acc == number:
            return (True, pos, cur_pos)
        cur_pos += 1
    return (False, None, None)


def find_contiguous(number, list):
    for i in range(len(list)):
        (res, start, end) = is_contiguous_ok(number, i, list)
        if res == True:
            return (start, end)
    return (None, None)


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Started')
    lv = LoadValues()
    numbers = lv.list_to_intlist()
    logging.debug(len(numbers))
    preamble = 25

    for i in range(len(numbers) - preamble - 1):
        number = numbers[i + preamble]
        candidates = numbers[i:i + preamble]
        logging.debug(len(candidates))
        res = is_sum(number, candidates)
        if not res:
            break
    print("Star 1 : ", number)

    (start, end) = find_contiguous(number, numbers)
    logging.debug((start, end))
    logging.debug(numbers[start:end + 1])
    min_val = min(numbers[start:end + 1])
    max_val = max(numbers[start:end + 1])

    print("Star 2 : ", min_val + max_val)

    logging.info('Finished')


##
if __name__ == '__main__':
    main()

import logging
import re
import cProfile

from loadValues import LoadValues

path_store_list = {}


def count_paths_list(start, end, adapters):
    logging.debug((start, end))
    if (start, end) in path_store_list:
        return path_store_list[(start, end)]
    nb = 0

    if start + 1 == end:
        return 1
    else:
        nb += count_paths_list(start + 1, end, adapters)
        if start + 2 <= end and adapters[start + 2] - adapters[start] <= 3:
            nb += count_paths_list(start + 2, end, adapters)
        if start + 3 <= end and adapters[start + 3] - adapters[start] <= 3:
            nb += count_paths_list(start + 3, end, adapters)

    path_store_list[(start, end)] = nb
    return nb


def main():
    lv = LoadValues()
    numbers = lv.list_to_intlist()
    logging.debug(len(numbers))
    adapters = [0] + numbers + [max(numbers) + 3]
    logging.debug(adapters)

    adapters.sort()
    logging.debug(adapters)
    diff = [adapters[i + 1] - adapters[i] for i in range(len(adapters) - 1)]
    logging.debug(diff)

    one = sum([i == 1 for i in diff])
    three = sum([i == 3 for i in diff])
    logging.debug((one, three, one * three))
    print("Star 1 : ", one * three)

    pr.enable()
    number = count_paths_list(0, len(adapters) - 1, adapters)
    print("Star 2 : ", number)
    pr.disable()
    logging.info('Finished')


##
if __name__ == '__main__':
    pr = cProfile.Profile()
    logging.basicConfig(level=logging.INFO)
    logging.info('Started')

    main()

    logging.info('Finished')
    pr.print_stats()

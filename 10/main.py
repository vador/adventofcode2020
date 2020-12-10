import logging
import re
import cProfile

from loadValues import LoadValues

chains_acc = []
chains_val = {}


def str_prefix(pos, adapters):
    str_prefix = "".join(["{:02d}".format(adapters[i]) for i in range(pos + 2)])
    return str_prefix


def is_valid_chain(adapters):
    diff = [adapters[i + 1] - adapters[i] for i in range(len(adapters) - 1)]
    # logging.debug(diff)
    return max(diff) <= 3


def how_many_for_pos(pos, adapters):
    tmp_adapt = adapters.copy()

    if (pos == 0):
        return 1
    cur_val = tmp_adapt.pop(pos)
    if len(tmp_adapt) == 0:
        return 1

    acc = 0
    str_pref = str_prefix(pos, adapters)

    if str_pref in chains_val:
        return chains_val[str_pref]

    if is_valid_chain(tmp_adapt):
        if pos >= 0:
            acc += how_many_for_pos(pos - 1, tmp_adapt)
    acc += how_many_for_pos(pos - 1, adapters)

    chains_acc.append((str_pref, acc))
    chains_val[str_pref] = acc
    logging.debug((pos, acc, adapters))

    return acc


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

    number = how_many_for_pos(len(adapters) - 2, adapters)
    print("Star 1 : ", one * three)

    print("Star 2 : ", number)
    logging.debug(sorted(list(set(chains_acc))))
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
    pr.print_stats()

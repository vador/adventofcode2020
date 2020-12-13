import logging
import re
import cProfile
import math

from loadValues import LoadValues

# Python 3.6
from functools import reduce


def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


# extended Euclides
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


def main():
    lv = LoadValues()
    lines = lv.strip_lines()

    earlier = int(lines[0])
    times = lines[1].split(',')
    logging.debug((earlier, times))
    best_time = earlier * 2
    bus_times = [(i, int(val)) for (i, val) in enumerate(times) if val != 'x']
    logging.debug(bus_times)

    bus = 0
    for (offset, t) in bus_times:
        first = (earlier // t + 1) * t
        logging.debug((earlier, t, first))
        if first < best_time:
            bus = t
            best_time = first
    logging.debug((bus, best_time))
    number = bus * (best_time - earlier)
    print("Star 1 : ", number)

    bus_period = [period for (offset, period) in bus_times]
    bus_offset = [(period - offset) % period for (offset, period) in bus_times]
    logging.debug(bus_period)
    logging.debug(bus_offset)

    number = chinese_remainder(bus_period, bus_offset)
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

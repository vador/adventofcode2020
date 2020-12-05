import logging

from loadValues import LoadValues


def calculate_id(row, column):
    return row * 8 + column


def dichotomy(range_value, which):
    (low, high) = range_value
    if which:
        return ((high + low) / 2 + 1, high)
    else:
        return (low, (high + low) / 2)


def find_row(binary_part, high):
    range_value = (0, high)
    for val in binary_part:
        range_value = dichotomy(range_value, val == 'B')
        logging.debug("New row " + str(range_value))
    return range_value


def find_alley(binary_part, high):
    range_value = (0, high)
    for val in binary_part:
        range_value = dichotomy(range_value, val == 'R')
        logging.debug("New alley " + str(range_value))
    return range_value


def find_seat(binary_part):
    row_seat = find_row(binary_part[:7], 127)[0]
    alley_seat = find_alley(binary_part[-3:], 7)[0]
    seat = calculate_id(row_seat, alley_seat)
    logging.info("New seat " + binary_part + str((seat, row_seat, alley_seat)))
    return seat


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Started')
    lv = LoadValues()
    lv.strip_lines()
    maxid = 0
    for boardingpass in lv.processed_values:
        curid = find_seat(boardingpass)
        if curid > maxid:
            maxid = curid

    print("Star1 :", maxid)

    logging.info('Finished')


##
if __name__ == '__main__':
    main()

import logging
import re
import cProfile

from loadValues import LoadValues


class Memory:
    mem = None
    masks = None

    def __init__(self):
        self.mem = {}

    def set_mask(self, mask):
        or_mask = ""
        and_mask = ""
        for bit in mask:
            if bit == 'X':
                or_mask += '0'
                and_mask += '1'
            else:
                or_mask += bit
                and_mask += bit
        logging.debug((or_mask, int(or_mask, 2)))
        logging.debug((and_mask, int(and_mask, 2)))
        self.masks = (int(or_mask, 2), int(and_mask, 2))
        return self.masks

    def set_mem(self, pos, value):
        (or_mask, and_mask) = self.masks
        new_value = (value & and_mask) | or_mask
        logging.debug((pos, value, new_value))
        self.mem[pos] = new_value
        return new_value

    def get_mem(self):
        return sum([self.mem[i] for i in self.mem])


def main():
    lv = LoadValues()
    lines = lv.strip_lines()

    mem = Memory()

    for line in lines:
        logging.debug(line)
        args = line.split(' = ')
        logging.debug(args)
        if args[0] == 'mask':
            mem.set_mask(args[1])
        else:
            logging.debug(("addr", args[0][4:-1]))
            mem_addr = int(args[0][4:-1])
            mem.set_mem(mem_addr, int(args[1]))

    number = mem.get_mem()

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

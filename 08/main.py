import logging
import re

from loadValues import LoadValues
from program import Program


def get_instructions(lines):
    instruction_list = []
    for line in lines:
        (op, val) = line.split(" ")
        val = int(val)
        instruction_list.append((op, val))
    return instruction_list


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Started')
    lv = LoadValues()
    lines = lv.strip_lines()

    instr = get_instructions(lines)
    prog = Program(instr)
    (_, ip, acc) = prog.does_terminate()
    print("Star 1 : ", acc)

    finished = None
    for (i, cur_instr) in enumerate(instr):
        if cur_instr[0] == 'nop' or cur_instr[0] == 'jmp':
            instr2 = instr.copy()
            if cur_instr[0] == 'nop':
                instr2[i] = ('jmp', cur_instr[1])
            else:
                instr2[i] = ('nop', cur_instr[1])
            (res, ip, acc) = Program(instr2).does_terminate()
            if res:
                finished = (ip, acc)
                break

    print("Star 2 : ", acc)

    logging.info('Finished')


##
if __name__ == '__main__':
    main()

import logging
import re

from loadValues import LoadValues


class Program:
    program = None
    acc = 0
    ip = 0
    max_instr = 0

    def __init__(self, instructions):
        self.program = instructions
        self.acc = 0
        self.ip = 0
        self.max_instr = len(instructions)

    def step(self):
        (op, val) = self.program[self.ip]
        if op == 'nop':
            self.ip += 1
        elif op == 'acc':
            self.acc += val
            self.ip += 1
        elif op == 'jmp':
            self.ip += val
        else:
            loggin.debug("Wrong op:" + op)
        return (self.ip, self.acc)

    def does_terminate(self):
        visited_addr = set()
        cur_ip = 0
        while cur_ip not in visited_addr:
            if cur_ip >= self.max_instr:
                return True, cur_ip, acc
            visited_addr.add(cur_ip)
            (cur_ip, acc) = self.step()
        return (False, cur_ip, acc)


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
    res = prog.does_terminate()
    print("Star 1 : ", res[2])

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

    print("Star 2 : ", finished)

    logging.info('Finished')


##
if __name__ == '__main__':
    main()

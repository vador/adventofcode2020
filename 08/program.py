import logging


class Program:
    program = None
    acc = None
    ip = None
    max_instr = None

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
            logging.debug("Wrong op:" + op)
        return self.ip, self.acc

    def does_terminate(self):
        visited_addr = set()
        cur_ip = 0
        while cur_ip not in visited_addr:
            if cur_ip >= self.max_instr:
                return True, cur_ip, self.acc
            visited_addr.add(cur_ip)
            (cur_ip, acc) = self.step()
        return False, cur_ip, self.acc

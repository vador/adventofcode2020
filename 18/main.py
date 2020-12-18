import logging
import re
import cProfile

from loadValues import LoadValues


def eval_rpn(expression):
    stack = []
    while len(expression) > 0:
        logging.debug((stack, expression))
        op = expression.pop(0)
        if op.isnumeric():
            stack.append(op)
        else:
            op1 = int(stack.pop())
            op2 = int(stack.pop())
            if op == '+':
                stack.append(op1 + op2)
            elif op == '*':
                stack.append(op1 * op2)
    return stack[0]


def shunting(expression, advanced=False):
    logging.debug(expression)
    stack = []
    output = []
    while len(expression) > 0:
        oper = expression.pop()
        if oper.isnumeric():
            output.append(oper)
        elif oper == '+':
            stack.append(oper)
        elif oper == '*':
            if advanced:
                while len(stack) > 0 and stack[-1] == '+':
                    output.append(stack.pop())
            stack.append(oper)
        elif oper == ')':
            stack.append(oper)
        elif oper == '(':
            oper2 = stack.pop()
            while oper2 != ')':
                output.append(oper2)
                oper2 = stack.pop()

        logging.debug((output, stack, expression))

    while len(stack) > 0:
        output.append(stack.pop())

    return output


def main():
    number = 0

    lv = LoadValues()
    lines = lv.strip_lines()

    # lines = ["1 + 2 * 3 + 4 * 5 + 6", "1 + ( 2 * 3 ) + ( 4 * ( 5 + 6 ) )","((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"]

    # expr = expr.replace('(', '( ')
    # expr = expr.replace(')', ' )')
    # ops = expr.split()
    # r1 = shunting(ops)
    # logging.debug(("r1:", r1))
    # r2 = eval_rpn(r1)
    # logging.debug(("r2:", r2))

    (acc1, acc2) = (0, 0)
    for line in lines:
        expr = line
        expr = expr.replace('(', '( ')
        expr = expr.replace(')', ' )')
        ops = expr.split()
        r1 = shunting(ops)
        r2 = eval_rpn(r1)
        logging.debug(("r1:", r1))
        logging.debug(("r2:", r2))
        acc1 += r2
        ops = expr.split()
        r1 = shunting(ops, advanced=True)
        r2 = eval_rpn(r1)
        acc2 += r2

    number = acc1

    print("Star 1 : ", number)
    number = acc2

    print("Star 2 : ", number)
    logging.info('Finished')


##
if __name__ == '__main__':
    pr = cProfile.Profile()
    logging.basicConfig(level=logging.INFO)
    logging.info('Started')
    pr.enable()

    main()
    pr.disable()

    logging.info('Finished')
    pr.print_stats()

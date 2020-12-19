import logging
import re
import cProfile

from loadValues import LoadValues


class Rule:
    ruleId = None
    value = None
    isLeaf = None

    def __init__(self, string):
        parse1 = string.split(': ')
        ruleId = parse1[0]
        self.ruleId = int(ruleId)
        if parse1[1] == '"a"' or parse1[1] == '"b"':
            self.isLeaf = True
            self.value = parse1[1][1]
        else:
            self.isLeaf = False
            parse2 = parse1[1].split(' | ')
            self.value = [[int(m) for m in val.split(' ')] for val in parse2]

    def __repr__(self):
        return "R:" + str(self.ruleId) + " " + str(self.isLeaf) + " " + str(self.value)


class RuleSet:
    rules = None

    def __init__(self):
        self.rules = {}

    def add(self, rule):
        self.rules[rule.ruleId] = rule

    def build_valid(self, message, node):
        currentRule = self.rules[node]
        if currentRule.isLeaf:
            if message[0] == currentRule.value:
                return {1}  # match at position 1
            else:
                return set()
        matches = set()
        for val in currentRule.value:  # we have one or 2 possibilities

            tmpMatch = {0}  # anchor
            for nextRule in val:
                newMatch = set()
                for pos in tmpMatch:
                    newMatch |= {pos + m for m in self.build_valid(message[pos:], nextRule)}
                tmpMatch = newMatch
            matches |= tmpMatch
        return matches


def main():
    number = 0

    lv = LoadValues("input.txt", groups=True)
    print(lv.raw_values)

    rules, messages = lv.raw_values
    RS = RuleSet()

    for line in lv.raw_values[0]:
        tmpRule = Rule(line)
        logging.debug(tmpRule)
        RS.add(tmpRule)
    logging.debug(RS.rules)

    logging.debug([RS.build_valid(m, 0) for m in messages])

    match = [len(m) in RS.build_valid(m, 0) for m in messages]

    number = sum(match)
    # CDEBUG:root:[{24}, set(), {24}, {24}, set(), set(), {24}, {24}, set(), {24}, {24}, {24}, {24}, set(), {24}, {24}, {24}, {24}, {24}, {24}, set(), {24}, {24}, {24}, set(), set(), {24}, set(), {24}, set(), {24}, set(), {24}, set(), {24}, {24}, {24}, {24}, {24}, {24}, set(), {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, set(), set(), set(), {24}, set(), set(), set(), {24}, set(), set(), {24}, set(), {24}, {24}, set(), set(), {24}, set(), {24}, {24}, set(), {24}, {24}, set(), {24}, set(), {24}, set(), {24}, set(), {24}, {24}, {24}, {24}, set(), {24}, set(), set(), set(), set(), {24}, {24}, {24}, {24}, {24}, {24}, set(), set(), {24}, {24}, set(), {24}, {24}, {24}, {24}, set(), {24}, {24}, {24}, {24}, {24}, {24}, set(), set(), {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, set(), {24}, {24}, set(), {24}, set(), set(), {24}, {24}, set(), set(), {24}, set(), {24}, {24}, {24}, {24}, set(), {24}, set(), set(), {24}, {24}, set(), set(), set(), set(), {24}, {24}, {24}, set(), {24}, set(), set(), {24}, {24}, set(), {24}, set(), set(), set(), {24}, set(), set(), {24}, {24}, {24}, set(), {24}, set(), set(), {24}, set(), set(), {24}, set(), set(), {24}, set(), set(), {24}, set(), set(), set(), {24}, set(), {24}, {24}, {24}, {24}, {24}, {24}, {24}, set(), {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, set(), {24}, {24}, set(), set(), {24}, set(), set(), set(), {24}, {24}, {24}, {24}, set(), {24}, {24}, set(), {24}, {24}, {24}, {24}, {24}, set(), set(), {24}, {24}, set(), {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, set(), set(), {24}, set(), set(), {24}, {24}, {24}, set(), {24}, {24}, set(), set(), {24}, {24}, set(), set(), {24}, set(), {24}, {24}, {24}, {24}, set(), {24}, {24}, {24}, {24}, {24}, set(), set(), {24}, set(), set(), {24}, {24}, {24}, set(), {24}, set(), set(), {24}, {24}, {24}, {24}, set(), {24}, {24}, {24}, {24}, {24}, set(), {24}, {24}, {24}, set(), {24}, {24}, {24}, set(), set(), {24}, {24}, {24}, {24}, {24}, set(), {24}, set(), set(), {24}, {24}, {24}, set(), {24}, {24}, {24}, set(), {24}, set(), set(), set(), set(), {24}, {24}, {24}, set(), {24}, set(), set(), {24}, {24}, {24}, {24}, set(), {24}, {24}, {24}, {24}, {24}, set(), {24}, set(), {24}, {24}, {24}, {24}, {24}, {24}, {24}, set(), set(), {24}, {24}, {24}, {24}, {24}, set(), {24}, set(), set(), {24}, {24}, set(), set(), {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, set(), {24}, {24}, {24}, {24}, set(), {24}, {24}, set(), set(), {24}, {24}, set(), {24}, {24}, set(), set(), set(), {24}, set(), set(), set(), {24}, set(), set(), {24}, {24}, set(), {24}, set(), set(), set(), {24}, set(), {24}, {24}, set(), {24}, set(), set(), {24}, {24}, set(), set(), {24}, {24}, {24}, set(), set(), set(), {24}, set(), {24}, set(), {24}, {24}, {24}, {24}, {24}, {24}, set(), set(), set(), {24}, {24}, set(), {24}, {24}, {24}, {24}, set(), set(), {24}, {24}, {24}, set(), set(), {24}, {24}, {24}, {24}, {24}, set(), {24}, {24}, set(), {24}, {24}, {24}, set(), set(), set(), set(), set()]
    # MDEBUG:root:[{24}, set(), {24}, {24}, set(), set(), {24}, {24}, set(), {24}, {24}, {24}, {24}, set(), {24}, {24}, {24}, {24}, {24}, {24}, set(), {24}, {24}, {24}, set(), set(), {24}, set(), {24}, set(), {24}, set(), {24}, set(), {24}, {24}, {24}, {24}, {24}, {24}, set(), {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, set(), set(), set(), {24}, set(), set(), set(), {24}, set(), set(), {24}, set(), {24}, {24}, set(), set(), {24}, set(), {24}, {24}, set(), {24}, {24}, set(), {24}, set(), {24}, set(), {24}, set(), {24}, {24}, {24}, {24}, set(), {24}, set(), set(), set(), set(), {24}, {24}, {24}, {24}, {24}, {24}, set(), set(), {24}, {24}, set(), {24}, {24}, {24}, {24}, set(), {24}, {24}, {24}, {24}, {24}, {24}, set(), set(), {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, set(), {24}, {24}, set(), {24}, set(), set(), {24}, {24}, set(), set(), {24}, set(), {24}, {24}, {24}, {24}, set(), {24}, set(), set(), {24}, {24}, set(), set(), set(), set(), {24}, {24}, {24}, set(), {24}, set(), set(), {24}, {24}, set(), {24}, set(), set(), set(), {24}, set(), set(), {24}, {24}, {24}, set(), {24}, set(), set(), {24}, set(), set(), {24}, set(), set(), {24}, set(), set(), {24}, set(), set(), set(), {24}, set(), {24}, {24}, {24}, {24}, {24}, {24}, {24}, set(), {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, set(), {24}, {24}, set(), set(), {24}, set(), set(), set(), {24}, {24}, {24}, {24}, set(), {24}, {24}, set(), {24}, {24}, {24}, {24}, {24}, set(), set(), {24}, {24}, set(), {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, set(), set(), {24}, set(), set(), {24}, {24}, {24}, set(), {24}, {24}, set(), set(), {24}, {24}, set(), set(), {24}, set(), {24}, {24}, {24}, {24}, set(), {24}, {24}, {24}, {24}, {24}, set(), set(), {24}, set(), set(), {24}, {24}, {24}, set(), {24}, set(), set(), {24}, {24}, {24}, {24}, set(), {24}, {24}, {24}, {24}, {24}, set(), {24}, {24}, {24}, set(), {24}, {24}, {24}, set(), set(), {24}, {24}, {24}, {24}, {24}, set(), {24}, set(), set(), {24}, {24}, {24}, set(), {24}, {24}, {24}, set(), {24}, set(), set(), set(), set(), {24}, {24}, {24}, set(), {24}, set(), set(), {24}, {24}, {24}, {24}, set(), {24}, {24}, {24}, {24}, {24}, set(), {24}, set(), {24}, {24}, {24}, {24}, {24}, {24}, {24}, set(), set(), {24}, {24}, {24}, {24}, {24}, set(), {24}, set(), set(), {24}, {24}, set(), set(), {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, {24}, set(), {24}, {24}, {24}, {24}, set(), {24}, {24}, set(), set(), {24}, {24}, set(), {24}, {24}, set(), set(), set(), {24}, set(), set(), set(), {24}, set(), set(), {24}, {24}, set(), {24}, set(), set(), set(), {24}, set(), {24}, {24}, set(), {24}, set(), set(), {24}, {24}, set(), set(), {24}, {24}, {24}, set(), set(), set(), {24}, set(), {24}, set(), {24}, {24}, {24}, {24}, {24}, {24}, set(), set(), set(), {24}, {24}, set(), {24}, {24}, {24}, {24}, set(), set(), {24}, {24}, {24}, set(), set(), {24}, {24}, {24}, {24}, {24}, set(), {24}, {24}, set(), {24}, {24}, {24}, set(), set(), set(), set(), set()]

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

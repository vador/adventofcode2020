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

    def build_rules(self, rules):
        for rule in rules:
            tmpRule = Rule(rule)
            logging.debug(tmpRule)
            self.add(tmpRule)

    def build_valid(self, message, node):
        currentRule = self.rules[node]
        if currentRule.isLeaf:
            if message and message[0] == currentRule.value:  # "if message" necessary if all message already consumed
                return {1}  # match one position 1
            else:
                return set()  # no match for this rule
        matches = set()
        for val in currentRule.value:  # we have 1,2 or 3 rules to match sequentially
            tmpMatch = {0}  # anchor
            for nextRule in val:
                newMatch = set()
                for pos in tmpMatch:
                    submatches = self.build_valid(message[pos:], nextRule)
                    newMatch.update({pos + m for m in submatches})
                tmpMatch = newMatch
            matches.update(tmpMatch)
        return matches


def main():
    number = 0

    lv = LoadValues("input.txt", groups=True)

    rules, messages = lv.raw_values

    RS = RuleSet()
    RS.build_rules(rules)
    logging.debug(RS.rules)

    res = [(len(m), RS.build_valid(m, 0)) for m in messages]
    logging.debug(res)
    match = [mlen in mset for (mlen, mset) in res]
    number = sum(match)

    print("Star 1 : ", number)

    rules.append("8: 42 | 42 8")
    rules.append("11: 42 31 | 42 11 31")

    RS = RuleSet()
    RS.build_rules(rules)
    logging.debug(RS.rules)

    res = [(len(m), RS.build_valid(m, 0)) for m in messages]
    logging.debug(res)
    match = [mlen in mset for (mlen, mset) in res]
    number = sum(match)

    print("Star 2 : ", number)


##
if __name__ == '__main__':
    pr = cProfile.Profile()
    logging.basicConfig(level=logging.INFO)
    logging.info('Started')
    pr.enable()

    main()
    pr.disable()

    logging.info('Finished')
    # pr.print_stats()

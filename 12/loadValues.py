import re


def parse_element(element):
    (quantity, compound) = element.strip().split(" ")
    return compound, int(quantity)


def parse_rule(element):
    (quantity_range, letter, password) = element.strip().split(" ")
    (qmin, qmax) = quantity_range.split("-")
    letter = letter[0]
    return (letter, (int(qmin), int(qmax))), password


def parse_passport(element):
    elems = element.split(" ")
    passport = {}
    for elem in elems:
        (k, v) = elem.split(":")
        passport[k] = v
    return passport


class LoadValues:
    file = './input.txt'
    raw_values = None
    processed_values = None

    def __init__(self, data=None, file=True, groups=False):
        if file:
            if data is not None:
                file_name = data
            else:
                file_name = self.file
            if groups:
                with open(file_name) as f:
                    self.raw_values = [line.split('\n') for line in f.read().strip().split("\n\n")]
            else:
                with open(file_name) as f:
                    self.raw_values = list(f)
        else:
            self.raw_values = list(data)

    def get_groups_from_lines(self, raw=None):
        if raw == None:
            raw = self.raw_values
        raw = self.strip_lines(raw)
        groups = []
        tmpgroup = []
        for line in raw:
            if len(line) >= 1:
                tmpgroup.append(line)
            else:
                groups.append(tmpgroup)
                tmpgroup = []
        if len(tmpgroup) >= 1:
            groups.append(tmpgroup)
        self.processed_values = groups
        return groups

    def passportlist_parse(self, raw=None):
        if raw == None:
            raw = self.raw_values
        raw = self.strip_lines(raw)
        passportlist = []
        tmppassport = ""
        for line in raw:
            if len(line) > 1:
                tmppassport += line + " "
            else:
                passportlist.append(tmppassport.strip())
                tmppassport = ""
        passportlist.append(tmppassport.strip())
        self.processed_values = passportlist

        passportlistkv = []
        for passport in passportlist:
            passportlistkv.append(parse_passport(passport))
        return passportlistkv

    def list_to_intlist(self, raw=None):
        if raw == None:
            raw = self.raw_values
        self.processed_values = [int(val) for val in raw]
        return self.processed_values

    def comma_list_to_intlist(self, raw=None):
        if raw == None:
            raw = self.raw_values
        self.processed_values = raw[0].split(",")
        return self.processed_values

    def get_3d_coords(self, raw=None):
        if raw is None:
            raw = self.raw_values
        coords = [tuple(map(int, list(re.findall(r'-?\d+', ln)))) for ln in raw]
        self.processed_values = coords
        return coords

    def get_rules(self, raw=None):
        rules = []
        if raw is None:
            raw = self.raw_values
        for ln in raw:
            rules.append(parse_rule(ln))
        return rules

    def get_reactions(self, raw=None):
        reactions = {}
        if raw is None:
            raw = self.raw_values
        for ln in raw:
            parse = ln.split(" =>")
            components = [parse_element(element) for element in parse[0].split(",")]
            (result, qr) = parse_element(parse[1])
            reactions[result] = ((result, qr), components)
        return reactions

    def get_digit_list(self, raw=None):
        if raw is None:
            raw = self.raw_values
        tmp = str(raw[0]).strip()
        return [int(i) for i in list(tmp)]

    def strip_lines(self, raw=None):
        if raw is None:
            raw = self.raw_values
        tmp = [line.strip() for line in raw]
        self.processed_values = tmp
        return tmp


if __name__ == '__main__':
    lv = LoadValues("input")

    print(lv.strip_lines())

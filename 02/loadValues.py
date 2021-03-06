import re


def parse_element(element):
    (quantity, compound) = element.strip().split(" ")
    return compound, int(quantity)


def parse_rule(element):
    (quantity_range, letter, password) = element.strip().split(" ")
    (qmin, qmax) = quantity_range.split("-")
    letter = letter[0]
    return (letter, (int(qmin), int(qmax))), password


class LoadValues:
    file = './input.txt'
    raw_values = None
    processed_values = None

    def __init__(self, data=None, file=True):
        if file:
            if data is not None:
                file_name = data
            else:
                file_name = self.file
            with open(file_name) as f:
                self.raw_values = list(f)
        else:
            self.raw_values = list(data)

    def list_to_intlist(self, raw=None):
        if raw is None:
            raw = self.raw_values
        self.processed_values = [int(val) for val in raw]
        return self.processed_values

    def comma_list_to_intlist(self, raw=None):
        if raw is None:
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

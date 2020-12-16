import logging
import re
import cProfile

from loadValues import LoadValues


class TicketValidator:
    fields = None

    def __init__(self):
        self.fields = {}

    def set_fields(self, field_list):
        for line in field_list:
            logging.debug(line)
            f_match = re.search(r'^([a-z ]*): (\d+)-(\d+) or (\d+)-(\d+)$', line)
            logging.debug(f_match.groups())
            f_name = f_match.group(1)
            f_mina = int(f_match.group(2))
            f_maxa = int(f_match.group(3))
            f_minb = int(f_match.group(4))
            f_maxb = int(f_match.group(5))
            logging.debug(("Fields split:", f_name, (f_mina, f_maxa), (f_minb, f_maxb)))
            self.fields[f_name] = ((f_mina, f_maxa), (f_minb, f_maxb))

    def is_value_valid_any(self, val):
        for field in self.fields:
            if self.is_value_valid_one_fields(field, val):
                return True
        return False

    def is_ticket_valid(self, ticket):
        invalid = 0
        for val in ticket:
            if not self.is_value_valid_any(val):
                invalid += val
        return (invalid == 0, invalid)

    def is_value_valid_one_fields(self, field_name, val):
        (mina, maxa), (minb, maxb) = self.fields[field_name]
        return (mina <= val <= maxa) or (minb <= val <= maxb)

    def get_valid_fields_for_value(self, val):
        return [field_name for field_name in self.fields if self.is_value_valid_one_fields(field_name, val)]


def main():
    number = 0

    lv = LoadValues(groups=True)

    tv = TicketValidator()
    tv.set_fields(lv.raw_values[0])
    ticket_list = lv.raw_values[2][1:]
    my_ticket = [int(val) for val in str(lv.raw_values[1][1:][0]).split(',')]
    logging.debug(ticket_list)
    valid_tickets = []
    for ticket in ticket_list:
        values = [int(i) for i in ticket.split(',')]
        logging.debug(("values :", values))
        (isValid, tmp) = tv.is_ticket_valid(values)
        number += tmp
        if isValid:
            valid_tickets.append(values)

    print("Star 1 : ", number)

    nb_fields = len(valid_tickets[0])
    field_val = 0

    valid_fields = [set(tv.fields.keys()) for i in range(nb_fields)]

    for ticket in valid_tickets:
        for (i, val) in enumerate(ticket):
            res = set(tv.get_valid_fields_for_value(val))
            valid_fields[i] = valid_fields[i].intersection(res)
    known_fields_val = {}
    known_fields_set = set()
    valid_fields = [(pos, valid) for (pos, valid) in enumerate(valid_fields)]
    valid_fields.sort(key=lambda val: len(val[1]), reverse=True)
    while len(valid_fields) > 0:
        cur_field = valid_fields.pop()
        (col, possible) = cur_field
        res = possible.difference(known_fields_set)
        res = res.pop()
        known_fields_val[res] = col
        known_fields_set.add(res)

    # calculate 2nd star
    number = 1
    for k in known_fields_val:
        if k[:9] == 'departure':
            number *= my_ticket[known_fields_val[k]]
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

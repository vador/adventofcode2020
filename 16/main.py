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
            (mina, maxa), (minb, maxb) = self.fields[field]
            if (mina <= val <= maxa) or (minb <= val <= maxb):
                return True
        return False

    def is_ticket_valid(self, ticket):
        invalid = 0
        for val in ticket:
            if not self.is_value_valid_any(val):
                invalid += val
        return (invalid == 0, invalid)


def main():
    number = 0

    lv = LoadValues(groups=True)

    tv = TicketValidator()
    tv.set_fields(lv.raw_values[0])
    ticket_list = lv.raw_values[2][1:]

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

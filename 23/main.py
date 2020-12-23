import cProfile
import logging


class Ring():
    ring = None
    next = None

    def __init__(self, str):
        values = [int(c) - 1 for c in str]

        nbval = len(values)
        self.ring = [0] * nbval
        curval = values[-1]
        for i in range(nbval):
            nextval = values[i]
            self.ring[curval] = nextval
            curval = nextval

    def valid_ring(self):
        return sum(self.output_order(1)) == 45

    def output_order(self, start):
        curval = start - 1
        output = [curval + 1]
        for i in range(len(self.ring) - 1):
            curval = self.ring[curval]
            output.append(curval + 1)
        return output

    def round(self, active):
        active = active - 1
        nbval = len(self.ring)
        # remove cups
        n1 = self.ring[active]
        n2 = self.ring[n1]
        n3 = self.ring[n2]
        n4 = self.ring[n3]

        dest = (active - 1) % nbval
        if dest in (n1, n2, n3):
            dest = (dest - 1) % nbval
        if dest in (n1, n2, n3):
            dest = (dest - 1) % nbval
        if dest in (n1, n2, n3):
            dest = (dest - 1) % nbval

        ndest = self.ring[dest]

        # New vals
        self.ring[active] = n4
        self.ring[dest] = n1
        self.ring[n3] = ndest

        return n4 + 1


def main():
    number = 0

    cups = '389125467'
    cups = '219748365'
    myR = Ring(cups)

    print(myR.output_order(2))
    active = int(cups[0])

    for i in range(100):
        active = myR.round(active)
        if not myR.valid_ring():
            print("error")
            break

    res = myR.output_order(1)
    number = ''.join([str(i) for i in res][1:])

    print("Star 1 : ", number)

    print("Star 2 : ", number)


##
if __name__ == '__main__':
    pr = cProfile.Profile()
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Started')
    pr.enable()

    played_hands = {}

    main()
    pr.disable()

    logging.info('Finished')
    # pr.print_stats()

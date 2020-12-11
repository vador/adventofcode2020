import logging
import re
import cProfile

from loadValues import LoadValues


class SeatPlan:
    NEIGHB = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
    FLOOR = "."
    EMPTY = "L"
    OCCUPIED = "#"
    seats = None
    people = None
    h = 0
    w = 0

    def __init__(self, seat_list):
        h = len(seat_list)
        w = len(seat_list[0])
        self.h = h
        self.w = w
        temp_seats = []
        temp_seats.append("." * (w + 2))
        for line in seat_list:
            nline = "." + line + "."
            temp_seats.append(nline)
        temp_seats.append("." * (w + 2))
        self.seats = temp_seats
        self.people = self.empty_board()

    def empty_board(self):
        people = [[0] * (self.w + 2) for i in range(self.h + 2)]
        return people

    def count_neighb(self, pos):
        (x, y) = pos
        cnt = 0
        for neighb in self.NEIGHB:
            (dx, dy) = neighb
            cnt += self.people[x + dx][y + dy]
        return cnt

    def new_seating(self):
        new_seat = self.empty_board()
        for x in range(1, self.h + 1):
            for y in range(1, self.w + 1):
                if self.seats[x][y] == self.EMPTY:
                    cnt = self.count_neighb((x, y))
                    if cnt == 0:
                        new_seat[x][y] = 1
                    elif cnt >= 4:
                        new_seat[x][y] = 0
                    else:
                        new_seat[x][y] = self.people[x][y]
        logging.debug(self.people)
        logging.debug(new_seat)

        self.people = new_seat
        return new_seat

    def count_neighb_line(self, pos):
        (x, y) = pos
        cnt = 0
        (h, w) = (self.h, self.w)
        for neighb in self.NEIGHB:
            (nx, ny) = (x, y)
            (dx, dy) = neighb
            while (0 <= nx + dx <= h + 1) and (0 <= ny + dy <= w + 1):
                if self.seats[nx + dx][ny + dy] == self.EMPTY:
                    cnt += self.people[nx + dx][ny + dy]
                    break
                (nx, ny) = (nx + dx, ny + dy)

        return cnt

    def new_seating_line(self):
        new_seat = self.empty_board()
        for x in range(1, self.h + 1):
            for y in range(1, self.w + 1):
                if self.seats[x][y] == self.EMPTY:
                    cnt = self.count_neighb_line((x, y))
                    if cnt == 0:
                        new_seat[x][y] = 1
                    elif cnt >= 5:
                        new_seat[x][y] = 0
                    else:
                        new_seat[x][y] = self.people[x][y]
        logging.debug(self.people)
        logging.debug(new_seat)

        self.people = new_seat
        return new_seat

    def array_seat(self):
        board = []
        for x in range(1, self.h - 1):
            lst = []
            for y in range(1, self.w - 1):
                if self.seats[x][y] == self.FLOOR:
                    lst.append(self.FLOOR)
                else:
                    if self.people[x][y]:
                        lst.append(self.OCCUPIED)
                    else:
                        lst.append(self.EMPTY)

            board.append("".join(lst))
        return board


def main():
    lv = LoadValues()
    seat_list = lv.strip_lines()
    logging.debug(seat_list)
    pr.enable()
    seats = SeatPlan(seat_list)
    logging.debug(seats.seats)

    cur_seat = seats.people
    new_seat = []
    while cur_seat != new_seat:
        cur_seat = new_seat
        new_seat = seats.new_seating()

    logging.debug("OK")
    number = sum([sum(line) for line in cur_seat])
    print("Star 1 : ", number)
    seats = SeatPlan(seat_list)

    seats = SeatPlan(seat_list)
    logging.debug(seats.seats)

    cur_seat = seats.people
    new_seat = []
    while cur_seat != new_seat:
        cur_seat = new_seat
        new_seat = seats.new_seating_line()
        print("\n".join(seats.array_seat()))
    number = sum([sum(line) for line in cur_seat])

    print("Star 2 : ", number)
    pr.disable()
    logging.info('Finished')


##
if __name__ == '__main__':
    pr = cProfile.Profile()
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Started')

    main()

    logging.info('Finished')
    # pr.print_stats()

import logging
import re
import cProfile


def transform(value, subject, modulo):
    return (value * subject) % modulo


def find_key(card, door):
    modulo = 20201227

    found = 0
    cnt = 1
    loop = 0
    cardloop = 0
    doorloop = 0

    while not (cardloop and doorloop):
        cnt = (cnt * 7) % modulo
        loop += 1
        if (cnt == card) and (cardloop == 0):
            cardloop = loop
        if (cnt == door) and (doorloop == 0):
            doorloop = loop
    key = 1
    for i in range(doorloop):
        key = transform(key, card, modulo)
    return cardloop, doorloop, key


def main():
    number = 0

    card, door = (15113849, 4206373)
    # card, door = (5764801, 17807724)

    cardloop, doorloop, number = find_key(card, door)
    print(cardloop, doorloop)
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
    pr.print_stats()

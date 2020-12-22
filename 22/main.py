import logging
import re
import cProfile
from collections import namedtuple, deque
from loadValues import LoadValues
import itertools


class GameCounter:
    nb = 0

    def __init__(self):
        self.nb = 1

    def inc_game(self):
        self.nb += 1

    def __repr__(self):
        return str(self.nb)


def parse_deck(lines):
    player = lines[0]
    deck = deque()
    for line in lines[1:]:
        deck.append(int(line))
    return (player, deck)


def do_game(deck1, deck2):
    while deck1 and deck2:
        a = deck1.popleft()
        b = deck2.popleft()
        if a < b:
            deck2.append(b)
            deck2.append(a)
        else:
            deck1.append(a)
            deck1.append(b)
    if deck1:
        return deck1
    else:
        return deck2


def score_deck(deck):
    cnt = 1
    score = 0
    while deck:
        score += cnt * deck.pop()
        cnt += 1
    return score


def get_winner_round(round, decks, gc):
    (a, b) = round
    (deck1, deck2) = decks
    logging.debug(("round: ", (round, decks)))
    if a <= len(deck1) and b <= len(deck2):
        gc.inc_game()
        deck1a = deque(itertools.islice(deck1, 0, a))
        deck2b = deque(itertools.islice(deck2, 0, b))
        (winner, _) = recursive_game(deck1a, deck2b, gc)
    else:
        if a > b:
            winner = 1
        else:
            winner = 2
    return winner


def recursive_game(deck1, deck2, gc):
    logging.debug(("new_game: ", gc, deck1, deck2))
    cur_game = str(gc)
    already_played = set()

    while True:
        # existing previous round -> player 1 wins game
        # TBD
        t = (tuple(deck1), tuple(deck2))
        if t in already_played:
            logging.debug(("Player 1 won : ", cur_game, " (already played position)"))
            return (1, deck1)
        else:
            already_played.add(t)

        a = deck1.popleft()
        b = deck2.popleft()
        winner_round = get_winner_round((a, b), (deck1, deck2), gc)
        if winner_round == 1:
            deck1.append(a)
            deck1.append(b)
            if len(deck2) == 0:
                logging.debug(("Player 1 won : ", cur_game))
                return (1, deck1)
        else:
            deck2.append(b)
            deck2.append(a)
            if len(deck1) == 0:
                logging.debug(("Player 2 won : ", cur_game))
                return (2, deck2)


def main():
    number = 0

    lv = LoadValues("input.txt", groups=True)

    decks = []
    for lines in lv.raw_values:
        (player, deck) = parse_deck(lines)
        decks.append(deck)

    print(decks)
    gc = GameCounter()

    winddeck = do_game(decks[0].copy(), decks[1].copy())
    number = score_deck(winddeck)
    print("Star 1 : ", number)

    print(score_deck(deque([7, 5, 6, 2, 4, 1, 10, 8, 9, 3])))
    deck1, deck2 = decks[0].copy(), decks[1].copy()
    winner, winddeck = recursive_game(deck1, deck2, gc)
    number = score_deck(winddeck)
    print("Star 2 : ", number)


##
if __name__ == '__main__':
    pr = cProfile.Profile()
    logging.basicConfig(level=logging.INFO)
    logging.info('Started')
    pr.enable()

    played_hands = {}

    main()
    pr.disable()

    logging.info('Finished')
    # pr.print_stats()

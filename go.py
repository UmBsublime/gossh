#!/usr/bin/env python3

import logging

from game.game import GoGame

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    game_id = input("Enter your game id or enter 'new' for a new game: ")
    if game_id == 'new':
        size = int(input("What size board would you like: "))

        try:
            g = GoGame(size)
        except ValueError:
            logger.warning('Invalid size {}'.format(size))
            print("Invalid size: {}. Valid sizes are 9, 13, 19".format(size))
            exit(1)
        color = input("black or white: ")
        while True:
            print(g)
            player = "White"
            if g.blacks_turn:
                player = "Black"

            p = input("{}, what is your move ('q' to quit)?: ".format(player)).split(' ')
            if p[-1] == 'q':
                exit()
            g.next_turn(p)



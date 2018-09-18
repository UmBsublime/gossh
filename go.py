#!/usr/bin/env python3

import logging

from game.game import GoGame

DB_URI = 'sqlite:///test.db'


if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    color = 'b'
    game_id = input("Enter your game id or enter nothing for a new game: ")
    if not game_id:
        game_id = -1
    else:
        color = input("Were you playing black or white stones ([b]lack/[w]hite) ?")
        if color not in ['b', 'w']:
            logger.error("You need to enter 'b' or 'w'")
            exit(1)
    size = input("What size board would you like, default is 9: ")
    if not size:
        size = 9

    try:
        if color is 'w':
            g = GoGame(int(size), DB_URI, is_black=False, game_id=int(game_id))
        else:
            g = GoGame(int(size), DB_URI, game_id=int(game_id))
    except ValueError:
        logger.warning('Invalid size {}'.format(size))
        print("Invalid size: {}. Valid sizes are 9, 13, 19".format(size))
        exit(1)
    color = input("black or white, default is black: ")
    while True:
        print(g)
        player = "White"
        if g.is_black:
            player = "Black"

        p = input("{}, what is your move ('q' to quit)?: ".format(player)).split(' ')
        if p[-1] == 'q':
            exit()
        g.next_turn(p)



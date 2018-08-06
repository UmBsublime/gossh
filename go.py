#!/usr/bin/env python3

import logging

#from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker

from game.game import GoGame, Move




# SQL init
DB_URI = 'sqlite:///test.db'
#engine = create_engine('sqlite:///test.db', echo=False)
#Base = declarative_base()
#Session = sessionmaker()
#Session.configure(bind=engine)

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    # Base.metadata.create_all(engine)
    #session = Session()

    #move = Move(pos_x=4, pos_y=5, color='black', map_id=1223)
    #session.add(move)
    #print(session.query(Move)[::])

    #t2 = session.query(Move).filter_by(pos_x=4)[-1]
    #session.delete(t2)
    #print(session.query(Move)[::])

    #exit()
    game_id = input("Enter your game id or enter nothing for a new game: ")

    if not game_id:
        size = int(input("What size board would you like: "))

        try:
            g = GoGame(size, 'sqlite:///test.db')
            exit()
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



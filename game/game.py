import logging
from string import ascii_lowercase

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from map.map import GoBoard
from map.tile import Position

logger = logging.getLogger(__name__)

Base = declarative_base()


class Move(Base):
    __tablename__ = 'move'
    id_ = Column(Integer, primary_key=True, autoincrement=True)
    pos_x = Column(Integer())
    pos_y = Column(Integer())
    color = Column(String(10))
    turn = Column(Integer())
    game_id = Column(Integer, ForeignKey('game.id_'))
    game = relationship("Game", back_populates="moves")

    def __repr__(self):
        return "<Move(id_='{}', pos_x='{}', pos_y='{}', color='{}', turn='{}', game_id='{}')>".format(
                                self.id_, self.pos_x, self.pos_y, self.color, self.turn, self.game_id)


class Game(Base):
    __tablename__ = 'game'
    id_ = Column(Integer, primary_key=True, autoincrement=True)
    black_turn = Column(Boolean(), default=True)
    size = Column(Integer(), default=9)
    moves = relationship("Move", back_populates="game")

    def __repr__(self):
        return "<Game(id_='{}', black_turn='{}', size='{}', moves='{}')>".format(
                                self.id_, self.black_turn, self.size, self.moves)

class GoGame:
    def __init__(self, size, db_uri, is_black=True, game_id=None):
        if size not in [9, 13, 19]:
            raise ValueError
        self.size = size
        self.board = GoBoard(size)
        self._win = False
        self.is_black = is_black
        self.db_uri = db_uri
        self.game_id = game_id
        self.turn = 0
        self._init_db()

    def _replay_game(self):
        pass

    def _create_game(self, game_id=None):
        if game_id:
            game = self.session.query(Game).filter(Game.id_ == game_id).one_or_none()
            print(type(game))
            if game:
                self._replay_game()
                return {'game': game, 'game_id': game.id_}
            else:
                return None
        else:
            game = Game(size=self.size, black_turn=True)
            self.session.add(game)
            self.session.commit()
            return {'game':game, 'game_id': game.id_}

    def _init_db(self):
        engine = create_engine(self.db_uri, echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker()
        Session.configure(bind=engine)
        self.session = Session()

        if self.game_id:
            game = self._create_game(self.game_id)
            if game:
                self.game = game['game']
                self.game_id = game['game_id']
                logger.info("Game with id {} found and initiated".format(self.game_id))
            else:
                logger.info("Could not find game with id: {}, creating a new one".format(self.game_id))
                game = self._create_game()
                self.game = game['game']
                self.game_id = game['game_id']
                logger.info("Game created, current game_id: {}".format(self.game_id))
                if not self.is_black:
                    self.is_black = True
                    logger.warning("It's not possible for you to be white, setting player to black")
        else:
            game = self._create_game()
            self.game = game['game']
            self.game_id = game['game_id']
            logger.info("Game created, current game_id: {}".format(self.game_id))


    def _validate_input(self, input_pos):
        try:
            assert isinstance(input_pos, list)
            assert len(input_pos) == 2
            assert isinstance(input_pos[0], str)
            assert isinstance(input_pos[1], str)

            # Check if we got a letter and a numbers only
            assert input_pos[0] in ascii_lowercase[:self.size] or \
                input_pos[0] in ' '.join([str(i) for i in list(range(1, self.size+1))])
            assert input_pos[1] in ascii_lowercase[:self.size] or \
                input_pos[1] in ' '.join([str(i) for i in list(range(1, self.size+1))])

            # Validate the number is not 0
            assert input_pos[0] is not '0' and input_pos[1] is not '0'

        except AssertionError:
            logging.warning("Invalid Input: {}".format(input_pos))
            return False

        return True

    def _convert_input(self, input_pos):
        if input_pos[0] in ascii_lowercase[:self.size]:
            p = Position(int(input_pos[1]), ascii_lowercase.index(input_pos[0])+1)
        else:
            p = Position(int(input_pos[0]), ascii_lowercase.index(input_pos[1])+1)

        logger.debug("Converted {} to {}".format(input_pos, p))
        return p

    def next_turn(self, input_pos):
        if self._validate_input(input_pos):
            p = self._convert_input(input_pos)
        else:
            logger.warning("You passed in an invalid input: {}".format(input_pos))
            return False
        if self.is_black:
            if self.board.play_black(p):
                logger.info("Black played at {}".format(input_pos))
                self.turn += 1
                move = Move(pos_x=p.pos_x, pos_y=p.pos_y, color='black', turn=self.turn, game_id=self.game_id)
                self.session.add(move)
                self.session.commit()
                self.is_black = not self.is_black
                return True
            else:
                logger.info("Black can not play at {}".format(input_pos))
        else:
            if self.board.play_white(p):
                logger.info("White played at {}".format(input_pos))
                self.turn += 1
                move = Move(pos_x=p.pos_x, pos_y=p.pos_y, color='white', turn=self.turn, game_id=self.game_id)
                self.session.add(move)
                self.session.commit()
                self.is_black = not self.is_black
                return True
            else:
                logger.info("White can not play at {}".format(input_pos))
        return False

    @property
    def win(self):
        return self._win

    @win.setter
    def win(self, wont_work):
        pass

    def __str__(self):
        return self.board.pretty_str()

    def __len__(self):
        return len(self.__str__())

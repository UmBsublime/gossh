import logging

from string import ascii_lowercase

from map.map import GoBoard
from map.tile import Position

logger = logging.getLogger(__name__)


class GoGame:
    def __init__(self, size):
        if size not in [9, 13, 19]:
            raise ValueError
        self.size = size
        self.board = GoBoard(size)
        self._win = False
        self.blacks_turn = True

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
        if self.blacks_turn:
            if self.board.play_black(p):
                logger.info("Black played at {}".format(input_pos))
                self.blacks_turn = not self.blacks_turn
                return True
            else:
                logger.info("Black can not play at {}".format(input_pos))
        else:
            if self.board.play_white(p):
                logger.info("White played at {}".format(input_pos))
                self.blacks_turn = not self.blacks_turn
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

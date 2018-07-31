import logging

logger = logging.getLogger(__name__)


class Position:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def __str__(self):
        return '({},{})'.format(self.pos_x, self.pos_y)


class BaseTile:

    def __init__(self, representation, can_move=False, can_traverse=False):
        self.representation = representation
        self.can_move = can_move
        self.can_traverse = can_traverse
        self._position = None

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_pos):
        self._position = new_pos

    def __str__(self):
        return self.representation


class ActorTile(BaseTile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, can_move=True, can_traverse=False, **kwargs)
        self.type = 'ActorTile'


class WallTile(BaseTile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, can_move=False, can_traverse=False, **kwargs)


class FloorTile(BaseTile):
    can_move_to = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, can_move=False, can_traverse=True, **kwargs)


class GoTile:
    def __init__(self, representation):
        self.representation = representation

    def __str__(self):
        return self.representation


class BoardTile(GoTile):

    def __init__(self, representation):
        super().__init__(representation)


class Stone(GoTile):

    def __init__(self, representation):
        super().__init__(representation)

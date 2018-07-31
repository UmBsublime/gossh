import logging
from string import ascii_lowercase

from map.tile import Position, Stone, BoardTile

logger = logging.getLogger(__name__)


class Map:

    def __init__(self):
        self.map_dict = {}

    def get_tile(self, position):
        try:
            ret = self.map_dict[position.pos_x][position.pos_y]
            return ret
        except KeyError:
            print('no tile here {}'.format(position))
            return None

    def init_tile(self, position):
        if position.pos_x not in self.map_dict:
            self.map_dict[position.pos_x] = {}
        self.map_dict[position.pos_x][position.pos_y] = None

    def del_tile(self, position):
        if position.pos_x in self.map_dict:
            self.map_dict[position.pos_x][position.pos_y] = None

    def set_tile(self, position, new_tile):
        if position.pos_x in self.map_dict:
                # print("x exist")
                self.map_dict[position.pos_x][position.pos_y] = new_tile
        else:
            self.map_dict[position.pos_x] = {position.pos_y: new_tile}

        return self.map_dict[position.pos_x][position.pos_y]

    def move_tile(self, src_pos, dst_pos, src_replacement_tile):
        if self._check_tile_exists(src_pos) and self._check_tile_exists(dst_pos):
            if self.get_tile(src_pos).can_move and self.get_tile(dst_pos).can_traverse:
                backup = self.get_tile(dst_pos)
                self.set_tile(dst_pos, self.get_tile(src_pos))
                self.set_tile(src_pos, src_replacement_tile)
                return backup
        return False

    def _check_tile_exists(self, position):

        try:
            if self.map_dict[position.pos_x][position.pos_y]:
                return True

        except KeyError:
            print('no tile here {}'.format(position))
            return False


class GoBoard:
    def __init__(self, size):
        self.size = size
        self.board = Map()
        self.stone_layer = Map()
        self._init_board()

    def _init_board(self):
        for i in range(self.size):
            for y in range(self.size):
                p = Position(i, y)
                if i and y != 0:
                    self.board.set_tile(p, BoardTile('┼'))
                self.stone_layer.init_tile(p)

        for i in range(self.size):
            px_left = Position(i, 0)
            py_top = Position(0, i)
            px_right = Position(i, self.size - 1)
            py_bottom = Position(self.size - 1, i)
            self.board.set_tile(px_left, BoardTile('├'))
            self.board.set_tile(py_top, BoardTile('┬'))
            self.board.set_tile(px_right, BoardTile('┤'))
            self.board.set_tile(py_bottom, BoardTile('┴'))

        self.board.set_tile(Position(0, 0), BoardTile('┌'))
        self.board.set_tile(Position(0, self.size-1), BoardTile('┐'))
        self.board.set_tile(Position(self.size-1, 0), BoardTile('└'))
        self.board.set_tile(Position(self.size-1, self.size-1), BoardTile('┘'))

    def _remove_stone(self, position):
        self.stone_layer.init_tile(Position(position.pos_x-1, position.pos_y-1))

    def _play(self, position, stone):
        new_pos = Position(position.pos_x - 1, position.pos_y - 1)
        if self.stone_layer.get_tile(new_pos):
            print('stone here {}'.format(position))
            return False
        return self.stone_layer.set_tile(new_pos, stone)

    def play_white(self, position):
        return self._play(position, Stone('●'))

    def play_black(self, position):
        return self._play(position, Stone('○'))

    def pretty_str(self):

        end_res = []
        _str = self.__str__().split()

        lines = ['─'.join(line) for line in _str]
        numbered_lines = ['{:<2}{}'.format(i + 1, line) for i, line in enumerate(lines)]
        letters = '  ' + ' '.join([ascii_lowercase[x] for x in range(self.size)])

        end_res.append(letters)
        end_res.extend(numbered_lines)
        return '\n'.join(end_res)

    def __str__(self):
        _str = ''
        for i in range(self.size):
            for y in range(self.size):
                tmp = str(self.board.get_tile(Position(i, y)))
                t = self.stone_layer.get_tile(Position(i, y))
                if t:
                    tmp = str(t)
                else:
                    pass
                _str += tmp
            if i is self.size - 1:
                break
            _str += '\n'
        return _str

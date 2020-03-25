""" Tiles for making courses. """

import numpy as np
from itertools import chain
from .tiles import BASE_GAME_TILES, PELOTON_EXPANSION_TILES


class Square(object):
    """ A space for cyclists side by side. """

    def __init__(self, index, curve, width=2, special=None):
        self.index = index
        self.curve = curve
        self.width = width
        self.special = special

        self.text = [None]*self.width
        self.positions = [None]*self.width
        self.occupants = [None]*self.width
        self.spaces = [None]*self.width

    @property
    def base_colour(self):
        if self.special == 'uphill':
            return '#bb6655'
        elif self.special == 'downhill':
            return '#5588dd'
        elif self.special == 'start':
            return '#dddddd'
        elif self.special == 'finish':
            return '#aa9922'
        elif self.special == 'cobbles':
            return '#6f5555'
        elif self.special == 'feed zone':
            return '#55cccc'
        elif self.special == 'breakaway':
            return '#777777'
        else:
            return '#777777'

    @property
    def profile_character(self):
        if self.special == 'cobbles':
            return '⣀⠒¨'
        elif self.special == 'feed zone':
            return '‗═˭'
        else:
            return '_—‾'

    @classmethod
    def from_char(cls, character, index, curve='straight'):
        if character == '=':
            return cls(index, curve)
        elif character == 'E':
            return cls(index, curve, width=3)
        elif character == 'u':
            return cls(index, curve, special='uphill')
        elif character == 'd':
            return cls(index, curve, special='downhill')
        elif character == 's':
            return cls(index, curve, special='start')
        elif character == 'S':
            return cls(index, curve, width=3, special='start')
        elif character == 'f':
            return cls(index, curve, special='finish')
        elif character == 'b':
            return cls(index, curve, special='breakaway')
        elif character == 'B':
            return cls(index, curve, width=3, special='breakaway')
        elif character == 'R':
            return cls(index, curve, width=3, special='feed zone')
        elif character == 'C':
            return cls(index, curve, special='cobbles')
        elif character == 'c':
            return cls(index, curve, width=1, special='cobbles')
        else:
            raise ValueError('unrecognized shorthand')


class Tile(object):
    """ A section containing several squares. """

    def __init__(self, squares, curve='straight'):
        if isinstance(squares, str):
            self._squares = self._parse_shorthand(squares)
        else:
            self._squares = squares
        self._curve = curve

    @property
    def squares(self):
        return self._squares

    @property
    def curve(self):
        return self._curve

    @property
    def distance(self):
        return sum(1 for square in self.squares if square.special not in ('start', 'finish'))

    @property
    def ascent(self):
        return sum(square.special=='uphill' for square in self.squares)

    @property
    def descent(self):
        return sum(square.special=='downhill' for square in self.squares)

    @classmethod
    def from_shorthand(cls, shorthand, index):
        if len(shorthand) == 6:
            return cls([Square.from_char(x, index+i)
                        for i,x in enumerate(shorthand)])
        elif len(shorthand) == 4:
            return cls([Square.from_char(x, index+i)
                        for i,x in enumerate(shorthand[:-1])])
        else:
            curve = shorthand[-1]
            squares = [Square.from_char(x, index+i, curve=curve)
                       for i,x in enumerate(shorthand[:-1])]
            return cls(squares, curve)


class Route(object):
    """ A complete course. """

    def __init__(self, tiles):
        self._tiles = tiles
        self._grid = None

    @property
    def tiles(self):
        return self._tiles

    @property
    def squares(self):
        return list(chain.from_iterable(tile.squares for tile in self.tiles))

    @property
    def distance(self):
        return sum(tile.distance for tile in self.tiles)

    @property
    def finish(self):
        return min(square.index for square in self.squares if square.special == 'f')

    @property
    def ascent(self):
        return sum(tile.ascent for tile in self.tiles)

    @property
    def descent(self):
        return sum(tile.descent for tile in self.tiles)

    @property
    def profile(self):
        square_heights = []
        km0 = 0
        for square in self.squares:
            if square.special == 'start':
                square_heights.append(0)
                km0 += 1
            elif square.special == 'uphill':
                square_heights.append(square_heights[-1] + 1)
            elif square.special == 'downhill':
                square_heights.append(square_heights[-1] - 1)
            elif square.special == 'finish':
                break
            else:
                square_heights.append(square_heights[-1])
        nadir = min(square_heights)
        lines = (max(square_heights) - nadir)//3 + 1

        char_grid = np.full([lines, self.distance+1], ' ')
        for i, (square, h) in enumerate(zip(self.squares[km0-1:], square_heights[km0-1:])):
            line = (h - nadir)//3
            h_in_line = (h - nadir)%3
            char_grid[line, i] = square.profile_character[h_in_line]

        profile_string = ''
        for line in char_grid[::-1]:
            for char in line:
                profile_string += char
            profile_string += '\n'
        return profile_string

    @classmethod
    def from_code(cls, code):
        """ Make a course from the lower/uppercase tile symbols. """

        if len(set(code)) < len(code):
            raise ValueError('repeated tile in code')

        index = 0
        tiles = []
        for symbol in code:
            if symbol.lower() in 'abcdefghijklmnopqrstu':
                tile = Tile.from_shorthand(BASE_GAME_TILES[symbol], index)
            elif symbol.lower() in 'vwxyz123456789':
                tile = Tile.from_shorthand(PELOTON_EXPANSION_TILES[symbol], index)
            else:
                continue
            tiles.append(tile)
            index += tile.distance

        return cls(tiles)

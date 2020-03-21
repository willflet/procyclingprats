""" Tiles for making courses. """

from itertools import chain
from .tiles import BASE_GAME_TILES


class Square(object):
    """ A space for cyclists side by side. """

    def __init__(self, index, curve, slope=None, width=2, special=None):
        self.index = index
        self.curve = curve
        self.slope = slope
        self.width = width
        self.special = special

        self.text = [None]*self.width
        self.positions = [None]*self.width
        self.occupants = [None]*self.width
        self.spaces = [None]*self.width

    @property
    def base_colour(self):
        if self.slope == 1:
            return '#bb6655'
        elif self.slope == -1:
            return '#5588dd'
        elif self.special == 'start':
            return '#dddddd'
        elif self.special == 'finish':
            return '#aa9922'
        else:
            return '#777777'

    @classmethod
    def from_char(cls, character, index, curve='straight'):
        if character == '=':
            return cls(index, curve)
        elif character == 'u':
            return cls(index, curve, slope=1)
        elif character == 'd':
            return cls(index, curve, slope=-1)
        elif character == 's':
            return cls(index, curve, special='start')
        elif character == 'f':
            return cls(index, curve, special='finish')
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
        return len(self.squares)

    @property
    def ascent(self):
        return sum(square.slope==1 for square in self.squares)

    @property
    def descent(self):
        return sum(square.slope==-1 for square in self.squares)

    @classmethod
    def from_shorthand(cls, shorthand, index):
        if len(shorthand) == 6:
            return cls([Square.from_char(x, index+i)
                        for i,x in enumerate(shorthand)])
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

    @classmethod
    def from_code(cls, code):
        """ Make a course from the lower/uppercase tile symbols. """

        if len(set(code.lower())) < len(code):
            raise ValueError('repeated tile in code')

        index = 0
        tiles = []
        for symbol in code:
            if symbol.lower() not in 'abcdefghijklmnopqrstu':
                continue
            tile = Tile.from_shorthand(BASE_GAME_TILES[symbol], index)
            tiles.append(tile)
            index += tile.distance

        return cls(tiles)

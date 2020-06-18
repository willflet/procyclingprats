""" Tiles for making courses. """

import numpy as np
from itertools import chain
from .tiles import BASE_GAME_TILES, PELOTON_EXPANSION_TILES, PROMOTIONAL_TILES, PERSONAL_TILES


CURVES = {'>':'L',')':'l','|':'S','(':'r','<':'R'}


class Square(object):
    """ A space for cyclists side by side. """

    def __init__(self, index, curve='|', width=2, special=''):
        self.index = index
        self.curve = CURVES[curve]
        self.width = width
        self.special = special

        self.text = [None]*self.width
        self.positions = [None]*self.width
        self.occupants = [None]*self.width
        self.spaces = [None]*self.width

    @property
    def base_colour(self):
        if 'uphill' in self.special:
            if 'steep' in self.special:
                return '#aa4433'
            else:
                return '#bb6655'
        elif 'downhill' in self.special:
            return '#5588dd'
        elif 'start' in self.special:
            return '#dddddd'
        elif 'finish' in self.special:
            return '#aa9922'
        elif 'cobbles' in self.special:
            return '#6f5555'
        elif 'feed zone' in self.special:
            return '#55cccc'
        elif 'crosswind' in self.special:
            return '#eeaa66'
        else:
            return '#777777'

    @property
    def profile_character(self):
        if 'cobbles' in self.special:
            return '⣀⠒¨'
        elif 'divided' in self.special:
            return '‗═˭'
        elif 'crosswind' in self.special:
            return '₊∗⁺'
        elif 'feed zone' in self.special:
            return 'ₒ∘°'
        else:
            return '_—‾'

    @classmethod
    def from_char(cls, character, index, curve='|'):
        # Flat
        if character == '-':
            return cls(index, curve, width=1)
        elif character == '=':
            return cls(index, curve, width=2)
        elif character == '+':
            return cls(index, curve, width=3)
        elif character == ':':
            return cls(index, curve, width=3, special='divided')

        # Ascent / Uphill
        elif character == 'a' or character == 'u':
            return cls(index, curve, width=1, special='uphill')
        elif character == 'A' or character == 'U':
            return cls(index, curve, width=2, special='uphill')
        elif character == 'M':
            return cls(index, curve, width=3, special='uphill')
        elif character == 'm':
            return cls(index, curve, width=3, special='divided uphill')
        elif character == 'Z':
            return cls(index, curve, width=2, special='steep uphill')

        # Descent / Downhill
        elif character == 'd' or character == 'v':
            return cls(index, curve, width=1, special='downhill')
        elif character == 'D' or character == 'V':
            return cls(index, curve, width=2, special='downhill')
        elif character == 'W':
            return cls(index, curve, width=3, special='downhill')
        elif character == 'w':
            return cls(index, curve, width=3, special='divided downhill')

        # Cobbles / Gravel
        elif character == 'c':
            return cls(index, curve, width=1, special='cobbles')
        elif character == 'C':
            return cls(index, curve, width=2, special='cobbles')
        elif character == 'G':
            return cls(index, curve, width=3, special='cobbles')
        elif character == 'g':
            return cls(index, curve, width=3, special='divided cobbles')

        # Feed zone / Refueling
        elif character == 'r':
            return cls(index, curve, width=1, special='feed zone')
        elif character == 'R':
            return cls(index, curve, width=2, special='feed zone')
        elif character == 'F':
            return cls(index, curve, width=3, special='feed zone')
        elif character == 'f':
            return cls(index, curve, width=3, special='divided feed zone')

        # Crosswind
        elif character == 'x':
            return cls(index, curve, width=2, special='crosswind right')
        elif character == 'X':
            return cls(index, curve, width=3, special='crosswind right')
        elif character == 'y':
            return cls(index, curve, width=2, special='crosswind left')
        elif character == 'Y':
            return cls(index, curve, width=3, special='crosswind left')

        # Start / Finish / Breakaway
        elif character == '(':
            return cls(index, curve, width=1, special='start')
        elif character == '[':
            return cls(index, curve, width=2, special='start')
        elif character == '{':
            return cls(index, curve, width=3, special='start')
        elif character == ')':
            return cls(index, curve, width=1, special='finish')
        elif character == ']':
            return cls(index, curve, width=2, special='finish')
        elif character == '}':
            return cls(index, curve, width=3, special='finish')
        elif character == 'b':
            return cls(index, curve, width=2, special='breakaway1')
        elif character == 'B':
            return cls(index, curve, width=3, special='breakaway2')

        else:
            raise ValueError('unrecognized shorthand')


class Tile(object):
    """ A section containing several squares. """

    def __init__(self, squares):
        self._squares = squares

    @property
    def squares(self):
        return self._squares

    @property
    def distance(self):
        return sum(1 for square in self.squares if 'start' not in square.special and 'finish' not in square.special)

    @property
    def ascent(self):
        return sum(('uphill' in square.special) for square in self.squares)

    @property
    def descent(self):
        return sum(('downhill' in square.special) for square in self.squares)

    @classmethod
    def from_shorthand(cls, shorthand, index):
        curve = shorthand[-1]
        squares = [Square.from_char(x, index+i, curve=curve)
                   for i,x in enumerate(shorthand[:-1])]
        return cls(squares)


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
        return min(square.index for square in self.squares if 'finish' in square.special)

    @property
    def ascent(self):
        return sum(tile.ascent for tile in self.tiles)

    @property
    def descent(self):
        return sum(tile.descent for tile in self.tiles)

    @property
    def profile(self):
        square_heights = [0]
        km0 = -1

        for square in self.squares:
            if 'start' in square.special:
                square_heights.append(0)
                km0 += 1
            elif 'uphill' in square.special:
                square_heights.append(square_heights[-1] + 1)
            elif 'downhill' in square.special:
                square_heights.append(square_heights[-1] - 1)
            elif 'finish' in square.special:
                break
            else:
                square_heights.append(square_heights[-1])

        nadir = min(square_heights)
        lines = (max(square_heights) - nadir)//3 + 1

        char_grid = np.full([lines, self.distance+1], ' ')
        if km0 == -1:
            line = (-nadir)//3
            h_in_line = (-nadir)%3
            char_grid[line, 0] = '_—‾'[h_in_line]

        for i, (square, h) in enumerate(zip(self.squares, square_heights[1:])):
            if i < km0: continue

            line = (h - nadir)//3
            h_in_line = (h - nadir)%3
            char_grid[line, i-km0] = square.profile_character[h_in_line]

        profile_string = ''
        for line in char_grid[::-1]:
            for char in line:
                profile_string += char
            profile_string += '\n'
        return profile_string

    @classmethod
    def from_code(cls, code):
        """ Make a course from the lower/uppercase tile symbols. """

        # if len(set(code)) < len(code):
        #     raise ValueError('repeated tile in code')

        index = 0
        tiles = []
        if code[0] in ('Aa1!'):
            for symbol in code:
                if symbol in BASE_GAME_TILES:
                    tile = Tile.from_shorthand(BASE_GAME_TILES[symbol], index)
                elif symbol in PELOTON_EXPANSION_TILES:
                    tile = Tile.from_shorthand(PELOTON_EXPANSION_TILES[symbol], index)
                elif symbol in PROMOTIONAL_TILES:
                    tile = Tile.from_shorthand(PROMOTIONAL_TILES[symbol], index)
                elif symbol in PERSONAL_TILES:
                    tile = Tile.from_shorthand(PERSONAL_TILES[symbol], index)
                else:
                    continue
                tiles.append(tile)
                index += tile.distance
        else:
            start_finish_lines_crossed = 0
            for symbol, next_symbol in zip(code, code[1:]+' '):
                if symbol in '>)(<|S123T':
                    if next_symbol == '|':
                        start_finish_lines_crossed += 1
                    continue

                square = Square.from_char(symbol, index)

                if next_symbol in '>)(<':
                    square.curve = CURVES[next_symbol]

                if start_finish_lines_crossed == 0:
                    square.special += ' start'
                elif start_finish_lines_crossed == 2:
                    square.special += ' finish'
                elif next_symbol in '123':
                    square.special += ' breakaway'+next_symbol

                if next_symbol == '|':
                    start_finish_lines_crossed += 1

                tile = Tile([square])
                tiles.append(tile)
                index += 1

        return cls(tiles)

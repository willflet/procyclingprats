""" Rider pieces and energy decks. """

from itertools import chain


COLOUR_DICT = dict(
    red='#990000',
    blue='#1133dd',
    green='#005500',
    black='#000000'
)

class Rider(object):
    """ A rider and energy deck. """

    def __init__(self, starting_deck, team):
        self._deck = starting_deck
        self._position = None
        self._team = team

    @property
    def team(self):
        return self._team

    @property
    def energy(self):
        return sum(card for card in self.deck)

    @property
    def position(self):
        return self._position

    @property
    def deck(self):
        return self._deck


class Rouleur(Rider):
    """ The Rouleur-type rider from the base game. """

    def __init__(self, team):
        self.name = 'rouleur'
        self.symbol = 'R'
        starting_deck = list(chain.from_iterable([x*3] for x in (3,4,5,6,7)))
        super().__init__(starting_deck, team)


class Sprinteur(Rider):
    """ The Sprinteur-type rider from the base game. """

    def __init__(self, colour):
        self.name = 'sprinteur'
        self.symbol = 'S'
        starting_deck = list(chain.from_iterable([x*3] for x in (2,3,4,5,9)))
        super().__init__(starting_deck, colour)


class Team(object):
    """ A team of several riders. """

    def __init__(self, colour, riders=['rouleur', 'sprinteur']):
        self.name = f'Team {colour.title()}'
        self.colour_name = colour
        self.colour = COLOUR_DICT[colour]
        self._riders = self._make_riders(riders)

    @property
    def riders(self):
        return self._riders

    def _make_riders(self, riders):
        _riders = []
        for rider in riders:
            if isinstance(rider, str):
                if rider == 'rouleur':
                    _riders.append(Rouleur(self))
                elif rider == 'sprinteur':
                    _riders.append(Sprinteur(self))
            else:
                _riders.append(rider)

        return _riders

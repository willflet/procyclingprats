""" Rider pieces and energy decks. """

from itertools import chain


COLOUR_DICT = dict(
    red='#990000',
    blue='#1133dd',
    green='#005500',
    black='#000000'
)


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
                if rider.lower() in ('r', 'rouleur'):
                    _riders.append(Rouleur(self))
                elif rider.lower() in ('s', 'sprinteur'):
                    _riders.append(Sprinteur(self))
                elif rider.lower() in ('b', 'baroudeur'):
                    _riders.append(Baroudeur(self))
                elif rider.lower() in ('f', 'finisseur'):
                    _riders.append(Finisseur(self))
                elif rider.lower() in ('g', 'grimpeur'):
                    _riders.append(Grimpeur(self))
                elif rider.lower() in ('p', 'puncheur'):
                    _riders.append(Puncheur(self))
                elif rider.lower() in ('v', 'veteran'):
                    _riders.append(Veteran(self))
                elif rider.lower() in ('d', 'descendeur'):
                    _riders.append(Descendeur(self))
            else:
                _riders.append(rider)

        return _riders


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
        starting_deck = list(int(x) for x in '333444555666777')
        super().__init__(starting_deck, team)


class Sprinteur(Rider):
    """ The Sprinteur-type rider from the base game. """

    def __init__(self, colour):
        self.name = 'sprinteur'
        self.symbol = 'S'
        starting_deck = list(int(x) for x in '222333444555999')
        super().__init__(starting_deck, colour)


class Baroudeur(Rider):
    """ The Rouleur-type rider from the base game. """

    def __init__(self, team):
        self.name = 'baroudeur'
        self.symbol = 'B'
        starting_deck = list(int(x) for x in '222333555666888')
        super().__init__(starting_deck, team)


class Finisseur(Rider):
    """ The Sprinteur-type rider from the base game. """

    def __init__(self, colour):
        self.name = 'finisseur'
        self.symbol = 'F'
        starting_deck = list(int(x) for x in '333344445555888')
        super().__init__(starting_deck, colour)


class Grimpeur(Rider):
    """ The Rouleur-type rider from the base game. """

    def __init__(self, team):
        self.name = 'grimpeur'
        self.symbol = 'G'
        starting_deck = list(int(x) for x in '333344445555777')
        super().__init__(starting_deck, team)


class Puncheur(Rider):
    """ The Sprinteur-type rider from the base game. """

    def __init__(self, colour):
        self.name = 'puncheur'
        self.symbol = 'P'
        starting_deck = list(int(x) for x in '222333444666888')
        super().__init__(starting_deck, colour)


class Veteran(Rider):
    """ The Rouleur-type rider from the base game. """

    def __init__(self, team):
        self.name = 'veteran'
        self.symbol = 'V'
        starting_deck = list(int(x) for x in '222333555666777')
        super().__init__(starting_deck, team)


class Descendeur(Rider):
    """ The Sprinteur-type rider from the base game. """

    def __init__(self, colour):
        self.name = 'descendeur'
        self.symbol = 'D'
        starting_deck = list(int(x) for x in '222333444666777')
        super().__init__(starting_deck, colour)

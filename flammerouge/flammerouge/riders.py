""" Rider pieces and energy decks. """

from itertools import chain
from .personalization import COLOUR_TO_NAMES


COLOUR_DICT = dict(
    red='#990000',
    blue='#1133dd',
    green='#005500',
    black='#000000',
    pink='#cc6688',
    purple='#664488'
)


class Team(object):
    """ A team of several riders. """

    def __init__(self, colour, riders=['R', 'S'], personalized=False):
        self.personalized = personalized
        self.colour = COLOUR_DICT[colour]
        self._riders = self._make_riders(riders)
        if personalized:
            self.name = COLOUR_TO_NAMES[colour]['team_name']
            self.riders[0].name = COLOUR_TO_NAMES[colour]['rider_0_name']
            self.riders[1].name = COLOUR_TO_NAMES[colour]['rider_1_name']
        else:
            self.name = f'Team {colour.title()}'

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
                elif rider.lower() in ('t', 'temeraire'):
                    _riders.append(Temeraire(self))
                elif rider.lower() in ('d', 'domestique'):
                    _riders.append(Domestique(self))
                elif rider.lower() in ('k', 'klassieker'):
                    _riders.append(Klassieker(self))
                elif rider.lower() in ('e', 'echappeur'):
                    _riders.append(Echappeur(self))
                elif rider.lower() in ('h', 'hercule'):
                    _riders.append(Hercule(self))
                elif rider.lower() in ('#', 'pelotonbot'):
                    _riders.append(PelotonBot(self))
                elif rider.lower() in ('@', 'breakawaybot'):
                    _riders.append(BreakawayBot(self))
                elif rider.lower() in ('x', 'xbot'):
                    _riders.append(XBot(self))
                elif rider.lower() in ('y', 'ybot'):
                    _riders.append(YBot(self))
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


class PelotonBot(Rider):
    """ A bot rider for the peloton expansion. """

    def __init__(self, team):
        self.name = 'pelotonbot'
        self.symbol = '#'
        starting_deck = list(int(x) for x in '33344455566677700')
        super().__init__(starting_deck, team)


class BreakawayBot(Rider):
    """ A bot rider for the peloton expansion. """

    def __init__(self, team):
        self.name = 'pelotonbot'
        self.symbol = '@'
        starting_deck = list(int(x) for x in '22233344455599900')
        super().__init__(starting_deck, team)


class XBot(Rider):
    """ A bot rider for an AI team. """

    def __init__(self, team):
        self.name = 'xbot'
        self.symbol = 'X'
        starting_deck = list(int(x) for x in '000000000000000')
        super().__init__(starting_deck, team)


class YBot(Rider):
    """ A bot rider for an AI team. """

    def __init__(self, team):
        self.name = 'ybot'
        self.symbol = 'Y'
        starting_deck = list(int(x) for x in '000000000000000')
        super().__init__(starting_deck, team)


class Rouleur(Rider):
    """ The diesel engine. """

    def __init__(self, team):
        self.name = 'Rouleur'
        self.symbol = 'R'
        starting_deck = list(int(x) for x in '333444555666777')
        super().__init__(starting_deck, team)


class Sprinteur(Rider):
    """ The speed freak. """

    def __init__(self, colour):
        self.name = 'Sprinteur'
        self.symbol = 'S'
        starting_deck = list(int(x) for x in '222333444555999')
        super().__init__(starting_deck, colour)


class Baroudeur(Rider):
    """ The breakaway specialist. """

    def __init__(self, team):
        self.name = 'Baroudeur'
        self.symbol = 'B'
        starting_deck = list(int(x) for x in '222333555666888')
        super().__init__(starting_deck, team)


class Finisseur(Rider):
    """ The opportunist. """

    def __init__(self, colour):
        self.name = 'Finisseur'
        self.symbol = 'F'
        starting_deck = list(int(x) for x in '333344445555888')
        super().__init__(starting_deck, colour)


class Grimpeur(Rider):
    """ The mountain goat. """

    def __init__(self, team):
        self.name = 'Grimpeur'
        self.symbol = 'G'
        starting_deck = list(int(x) for x in '333344445555777')
        super().__init__(starting_deck, team)


class Puncheur(Rider):
    """ The fireworks. """

    def __init__(self, colour):
        self.name = 'Puncheur'
        self.symbol = 'P'
        starting_deck = list(int(x) for x in '222333444666888')
        super().__init__(starting_deck, colour)


class Veteran(Rider):
    """ The old hand. """

    def __init__(self, team):
        self.name = 'Veteran'
        self.symbol = 'V'
        starting_deck = list(int(x) for x in '222333555666777')
        super().__init__(starting_deck, team)


class Temeraire(Rider):
    """ The daredevil. """

    def __init__(self, colour):
        self.name = 'Temeraire'
        self.symbol = 'T'
        starting_deck = list(int(x) for x in '222333445566777')
        super().__init__(starting_deck, colour)


class Domestique(Rider):
    """ The trusty lieutenant. """

    def __init__(self, colour):
        self.name = 'Domestique'
        self.symbol = 'D'
        starting_deck = list(int(x) for x in '333444455556666')
        super().__init__(starting_deck, colour)


class Klassieker(Rider):
    """ The classics specialist. """

    def __init__(self, colour):
        self.name = 'Klassieker'
        self.symbol = 'K'
        starting_deck = list(int(x) for x in '222244445556699')
        super().__init__(starting_deck, colour)


class Echappeur(Rider):
    """ The local hero. """

    def __init__(self, colour):
        self.name = 'Echappeur'
        self.symbol = 'E'
        starting_deck = list(int(x) for x in '222333555666778')
        super().__init__(starting_deck, colour)


class Hercule(Rider):
    """ The strongman. """

    def __init__(self, colour):
        self.name = 'Hercule'
        self.symbol = 'H'
        starting_deck = list(int(x) for x in '222333344666699')
        super().__init__(starting_deck, colour)

""" Interactive board game. """

import random
from .riders import Team
from .route import Route


AFFIRMATIVE_RESPONSES = ('y', 'yes', 't', 'true')
NEGATIVE_RESPONSES = ('n', 'no', 'f', 'false')


class GameState(object):
    """ Full state of the game. """

    def __init__(self, route, teams):
        self.route = route
        self.teams = teams
        self._rider_precedence = random.sample(
            [rider for team in teams for rider in team.riders],
            k=sum(len(team.riders) for team in teams)
        )

    @property
    def rider_precedence(self):
        return self._rider_precedence

    def dump(self):
        ...

    def dumps(self):
        ...

    def load(self, json_file):
        ...

    def loads(self, json_string):
        ...


class Game(object):
    """ An interactive game of Flamme Rouge. """

    def __init__(self):
        ...

    def setup(self, colour_choices=('red', 'blue', 'black', 'green')):
        teams = []
        for colour in colour_choices:
            using = input(f'\nIs someone using the {colour} team? (y/n)\n')

            while True:
                if using.lower() in AFFIRMATIVE_RESPONSES:
                    # riders = input(
                    #     f'\nWhat riders is the {colour} team using?\n'
                    #     '    (Default: rouleur sprinteur)\n'
                    # ).split()
                    # if not riders:
                    riders = ['rouleur', 'sprinteur']
                    teams.append(Team(colour, riders))
                    break
                elif using.lower() in NEGATIVE_RESPONSES:
                    break
                else:
                    using = input("Didn't understand, try again please:\n")

        route_code = input('\nEnter a code to define the course:\n')
        route = Route.from_code(route_code)

        self.state = GameState(route, teams)

        print(
            f'\n\n\n=============================================='
            f'\nReady to race!',
            f'\nCourse is {route.distance} squares long',
            f'There are {route.ascent} uphill squares and {route.descent} downhill.',
            f'',
            f'Teams are:',
            sep='\n'
        )
        for team in teams:
            print(f'\n  {team.name} ({team.colour_name}):', end='\n    ')
            print('\n    '.join(r.name for r in team.riders))

        confirmation = input('\n\nIs this correct? (Y/n)\n')
        while True:
            if confirmation.lower() in AFFIRMATIVE_RESPONSES:
                break
            elif not confirmation:
                break
            elif confirmation.lower() in NEGATIVE_RESPONSES:
                self.setup()
            else:
                using = input("Didn't understand, try again please:\n")

        rotation = input('\nBoard rotation? (Default 0 degrees)\n')
        if rotation:
            self.starting_orientation = int(rotation)
        else:
            self.starting_orientation = 0

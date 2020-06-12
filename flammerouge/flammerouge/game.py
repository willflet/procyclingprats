""" Interactive board game. """

import random
from copy import deepcopy
from .riders import Team
from .route import Route
from .board import Board
from .presets import COURSES, DUPLICATE_NAMES, LONG_STAGES


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
        self.setup()

    def setup(self, colour_choices=('red', 'blue', 'black', 'green', 'pink', 'purple')):
        teams = []
        for colour in colour_choices:
            using = input(f'\nIs someone using the {colour} team? (y/n)\n')

            while True:
                if not using:
                    using = input()
                elif using.lower() in AFFIRMATIVE_RESPONSES:
                    riders = (
                        input(
                            f'\nWhat riders is the {colour} team using?\n'
                            '    (Default: rouleur sprinteur)\n'
                        ) or 'r s'
                    ).split()
                    while True:
                        if len(riders) == 2:
                            break
                        else:
                            riders = (
                                input(
                                    f'\nExpected two riders (space-separated); try again.\n'
                                ) or 'r s'
                            ).split()
                    teams.append(Team(colour, riders, personalized=True))
                    break
                elif using.lower() in NEGATIVE_RESPONSES:
                    break
                else:
                    using = input("Didn't understand, try again please:\n")

        route_code = input('\nEnter a stage name or a code to define the course. Or type "show" to see presets\n')
        if route_code == 'show':
            for key in COURSES:
                print(key)
                route = Route.from_code(COURSES[key][0])
                print(route.profile)
            route_code = input('\nEnter a stage name or a code to define the course.\n')
        key = route_code.lower().replace(' ','').replace('-','').replace("'",'')
        if key in COURSES:
            route = Route.from_code(COURSES[key][0])
            rotation = COURSES[key][1]
        elif key in DUPLICATE_NAMES:
            route = Route.from_code(COURSES[DUPLICATE_NAMES[key]][0])
            rotation = COURSES[DUPLICATE_NAMES[key]][1]
        else:
            rotation = int(input(f'\nManual stage creation mode using code "{route_code}".'
                                 f'\nBearing of first tile? (Default 0 degrees)\n') or 0)
            route = Route.from_code(route_code)

        markers = (input('\nWhat intermediate points are there?\n') or '').upper().split()

        print('Course length: {}\n\n'.format(route.distance),
            route.profile,
            "0''''''''10''''''''20''''''''30''''''''40''''''''50''''''''60''''''''70''''''''80",
            f'\nReady to race! Riders are:',
            sep='\n'
        )
        for team in teams:
            print(f'\n  {team.name.ljust(12)}:', end=' ')
            print('\n                '.join(
                f'{rider.symbol} ({rider.name})'
                for rider in team.riders)
            )

        confirmation = input('\nIs this correct? (Y/n)\n')
        while True:
            if confirmation.lower() in AFFIRMATIVE_RESPONSES:
                break
            elif not confirmation:
                break
            elif confirmation.lower() in NEGATIVE_RESPONSES:
                self.setup()
            else:
                using = input("Didn't understand, try again please:\n")

        self.board = Board()
        self.board.draw_route(route, rotation)
        self.board.place_markers(markers)

        self.state = GameState(route, teams)
        self.initial_state = deepcopy(self.state)

        for rider, square in zip(self.state.rider_precedence, route.squares[8:]):
            self.board.place_rider(rider, square, lane=square.width-1)

        self.board.activate()


if __name__ == '__main__':
    Game()

""" Interactive board game. """

from copy import deepcopy
import numpy as np
import tkinter as tk
from .tiles import GEOMETRIES, STRAIGHT_L, LANE_W, SHARP_R, WIDE_R
from .game import Game


SQUARE_SIZE = 18

sin45 = (2**0.5)/2
cos45 = sin45
sin22 = ((2 - (2**0.5))**0.5)/2
cos22 = ((2 + (2**0.5))**0.5)/2


class Board(object):

    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry(str(2000)+'x'+str(2000))
        self._c = tk.Canvas(self.window, width=2000, height=2000, bg='#83c750')
        self._c.pack()
        self._c.bind("<ButtonPress-1>", self.scroll_start)
        self._c.bind("<B1-Motion>", self.scroll_move)

        self.mouse_state = None

    def activate(self):
        self.window.mainloop()

    def draw_route(self, route, starting_orientation=0):
        position = np.array([[1000.0,-1000.0]])/SQUARE_SIZE
        orientation = starting_orientation
        for square in route.squares:
            rotate = self.rotation_matrix(orientation)
            square.positions[0] = position + [STRAIGHT_L/4, -LANE_W/2] @ rotate
            square.positions[0] *= SQUARE_SIZE
            square.positions[1] = position + [STRAIGHT_L/4, LANE_W/2] @ rotate
            square.positions[1] *= SQUARE_SIZE

            self.draw_space(square, 0, position, orientation)
            self.draw_space(square, 1, position, orientation)

            if square.curve == 'straight':
                position += 1.05*([STRAIGHT_L, 0.0] @ rotate)
            elif square.curve == 'L':
                position += 1.05*([SHARP_R*sin45, SHARP_R-SHARP_R*cos45] @ rotate)
                orientation += 45
            elif square.curve == 'R':
                position += 1.05*([SHARP_R*sin45, -(SHARP_R-SHARP_R*cos45)] @ rotate)
                orientation -= 45
            elif square.curve == 'l':
                position += 1.05*([WIDE_R*sin22, WIDE_R-WIDE_R*cos22] @ rotate)
                orientation += 22.5
            elif square.curve == 'r':
                position += 1.05*([WIDE_R*sin22, -(WIDE_R-WIDE_R*cos22)] @ rotate)
                orientation -= 22.5

    def draw_space(self, square, lane, position, orientation):
        rotate = self.rotation_matrix(orientation)

        key = f'{square.curve}_{lane}'
        geometry = (GEOMETRIES[key] @ rotate + position) * SQUARE_SIZE
        geometry[:,1] *= -1
        square.spaces[lane] = self._c.create_polygon(
            geometry.flatten().tolist(),
            fill=square.base_colour,
            outline='#404040',
            width=(SQUARE_SIZE/5)
        )
        func = lambda event: self.click_space(event, square, lane)
        self._c.tag_bind(square.spaces[lane], '<Button-1>', func)

    def place_rider(self, rider, square, lane):
        if square.occupants[lane] is not None:
            print('clicked an already-occupied space')
        else:
            square.occupants[lane] = rider
            rider._position = (square, lane)
            self._c.itemconfig(square.spaces[lane], fill=rider.team.colour)
            square.text[lane] = self._c.create_text(
                square.positions[lane][0,0],
                -square.positions[lane][0,1],
                text=rider.symbol,
                fill='#ffffff'
            )
            self.mouse_state = None

    def pick_up_rider(self, rider):
        if rider is None:
            print('clicked an empty space')
        else:
            square, lane = rider.position
            square.occupants[lane] = None
            rider._position = None
            self._c.itemconfig(square.spaces[lane], fill=square.base_colour)
            self._c.delete(square.text[lane])
            self.mouse_state = rider

    def click_space(self, event, square, lane):
        rider = square.occupants[lane]
        if self.mouse_state is None:
            print('empty-handed, picking up')
            self.pick_up_rider(rider)
        else:
            print(f"placing {self.mouse_state.team.name}'s {self.mouse_state.name}")
            self.place_rider(self.mouse_state, square, lane)

    def scroll_start(self, event):
        self._c.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self._c.scan_dragto(event.x, event.y, gain=1)

    @staticmethod
    def rotation_matrix(angle):
        return np.array([
            [ np.cos(angle*np.pi/180),  np.sin(angle*np.pi/180)],
             [-np.sin(angle*np.pi/180),  np.cos(angle*np.pi/180)]
        ])


def main():

    game = Game()
    game.setup()

    initial_state = deepcopy(game.state)

    board = Board()
    board.draw_route(game.state.route, game.starting_orientation)

    for rider, square in zip(game.state.rider_precedence, game.state.route.squares[8:]):
        board.place_rider(rider, square, lane=0)

    board.activate()


if __name__ == '__main__':
    main()

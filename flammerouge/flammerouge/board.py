""" Interactive board game. """

import numpy as np
import tkinter as tk
import pygame
import os
from .tiles import GEOMETRIES, STRAIGHT_L, LANE_W, SHARP_R, WIDE_R


SQUARE_SIZE = 17

sin45 = (2**0.5)/2
cos45 = sin45
sin22 = ((2 - (2**0.5))**0.5)/2
cos22 = ((2 + (2**0.5))**0.5)/2


class Board(object):

    def __init__(self, audio_path='./commentary'):
        self.window = tk.Tk()
        self.window.geometry(str(2000)+'x'+str(2000))
        self._c = tk.Canvas(self.window, width=2000, height=2000, bg='#83c750')
        self._c.pack()
        self._c.bind('<ButtonPress-1>', self.scroll_start)
        self._c.bind('<B1-Motion>', self.scroll_move)

        self.audio_path = audio_path
        self.make_soundboard()

        self.mouse_state = None
        self.pygame = pygame
        self.pygame.init()
        self.pygame.mixer.init(frequency=70000)
        self.window.focus_set()

    def make_soundboard(self):
        self.window.bind("q", self.attaque_de_pierre_rolland)
        self.window.bind("w", lambda event: self.play_audio('hes_racing_on.ogg'))
        self.window.bind("e", lambda event: self.play_audio('fed_up_forming_alliances.ogg'))
        self.window.bind("r", lambda event: self.play_audio('gets_his_head_down.ogg'))
        self.window.bind("t", lambda event: self.play_audio('what_a_finish.ogg'))
        self.window.bind("y", lambda event: self.play_audio('yeeesss_he_takes_it.ogg'))
        self.window.bind("a", lambda event: self.play_audio('nobody_wants_to_chase.ogg'))
        self.window.bind("s", lambda event: self.play_audio('oh_here_we_go_then.ogg'))
        self.window.bind("d", lambda event: self.play_audio('oh_drama_here.ogg'))
        self.window.bind("f", lambda event: self.play_audio('everyone_has_to_be_tired_here.ogg'))
        self.window.bind("g", lambda event: self.play_audio('oh_nightmare_scenario.ogg'))
        self.window.bind("h", lambda event: self.play_audio('oh_heartbreak_here.ogg'))
        self.window.bind("z", lambda event: self.play_audio('absolutely_fantastic.ogg'))
        self.window.bind("x", lambda event: self.play_audio('loved_that.ogg'))
        self.window.bind("c", lambda event: self.play_audio('chuckle.ogg'))
        self.window.bind("v", lambda event: self.play_audio('oh_chapeau_sir.ogg'))

    def activate(self):
        self.window.mainloop()

    def draw_route(self, route, starting_orientation=0):
        position = np.array([[1000.0,-1000.0]])/SQUARE_SIZE
        orientation = starting_orientation

        last_colour = '#dddddd'
        last_width = route.squares[0].width
        for square in route.squares:

            rotate = self.rotation_matrix(orientation)

            if square.width == 1:
                square.positions[0] = position + [STRAIGHT_L/4, 0] @ rotate
            elif square.width == 2:
                square.positions[0] = position + [STRAIGHT_L/4, -LANE_W/2] @ rotate
                square.positions[1] = position + [STRAIGHT_L/4, LANE_W/2] @ rotate
            elif square.width == 3:
                square.positions[0] = position + [STRAIGHT_L/4, -LANE_W] @ rotate
                square.positions[1] = position + [STRAIGHT_L/4, 0] @ rotate
                square.positions[2] = position + [STRAIGHT_L/4, LANE_W] @ rotate

            for i in range(square.width):
                square.positions[i] *= SQUARE_SIZE

            for lane in range(square.width):
                self.draw_space(square, lane, position, orientation)

            if square.base_colour != last_colour:
                border_geom = np.array([
                    [-0.15, (max(last_width, square.width)/2 + 0.3)*LANE_W],
                    [-0.15, (-max(last_width, square.width)/2 - 0.3)*LANE_W],
                    [0.15, (-max(last_width, square.width)/2 - 0.3)*LANE_W],
                    [0.15, (max(last_width, square.width)/2 + 0.3)*LANE_W]
                ])
                border_geom = (border_geom @ rotate + position) * SQUARE_SIZE
                border_geom[:,-1] *= -1
                colour = last_colour if last_colour != '#777777' else square.base_colour
                border = self._c.create_polygon(
                    border_geom.flatten().tolist(),
                    fill=colour,
                    outline='#404040',
                    width=(SQUARE_SIZE/10)
                )
                self._c.lift(border)
            last_colour = square.base_colour
            last_width = square.width

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

        key = f'{square.curve}_{lane*2 - square.width + 3}'
        geometry = (GEOMETRIES[key] @ rotate + position) * SQUARE_SIZE
        geometry[:,1] *= -1
        if square.special == 'breakaway' and lane != square.width-1:
            colour = '#dddddd'
        else:
            colour = square.base_colour
        square.spaces[lane] = self._c.create_polygon(
            geometry.flatten().tolist(),
            fill=colour,
            outline='#404040',
            width=(SQUARE_SIZE/5)
        )
        func = lambda event: self.click_space(event, square, lane)
        self._c.tag_bind(square.spaces[lane], '<Button-1>', func)

    def place_rider(self, rider, square, lane):
        if square.occupants[lane] is None:
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
        if rider is not None:
            square, lane = rider.position
            square.occupants[lane] = None
            rider._position = None
            if square.special == 'breakaway' and lane != square.width-1:
                colour = '#dddddd'
            else:
                colour = square.base_colour
            self._c.itemconfig(square.spaces[lane], fill=colour)
            self._c.delete(square.text[lane])
            self.mouse_state = rider

    def change_background_with_delay(self, colour_sequence):
        self._c.configure(bg=colour_sequence[self.colour_index])
        self.colour_index += 1
        if self.colour_index >= len(colour_sequence):
            return
        else:
            self.window.after(494, lambda: self.change_background_with_delay(colour_sequence))

    def attaque_de_pierre_rolland(self, event):
        self.play_audio('attaque_de_pierre_rolland.ogg')

        self.colour_index = 0
        colour_sequence = ['#ffdd00', '#527439']*7 + ['#ffdd00', '#83c750']

        self.window.after(1270, lambda: self.change_background_with_delay(colour_sequence))

    def play_audio(self, filename):
        self.pygame.mixer.music.load(os.path.join(self.audio_path, filename))
        self.pygame.mixer.music.play()

    def click_space(self, event, square, lane):
        rider = square.occupants[lane]
        if self.mouse_state is None:
            self.pick_up_rider(rider)
        else:
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

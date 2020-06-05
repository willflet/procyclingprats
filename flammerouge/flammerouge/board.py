""" Interactive board game. """

import numpy as np
import tkinter as tk
import pygame
import os
from .tiles import GEOMETRIES, STRAIGHT_L, LANE_W, SHARP_R, WIDE_R


AUDIO_PATH = '/mnt/c/Users/magic/OneDrive/Documents/Code Projects/Projects/procyclingprats/flammerouge/commentary'

SQUARE_SIZE = 17

sin45 = (2**0.5)/2
cos45 = sin45
sin22 = ((2 - (2**0.5))**0.5)/2
cos22 = ((2 + (2**0.5))**0.5)/2


class Board(object):

    def __init__(self, audio_path=AUDIO_PATH):
        self._w = tk.Tk()
        self._w.geometry(str(2000)+'x'+str(2000))
        self._c = tk.Canvas(self._w, width=2000, height=2000, bg='#83c750')
        self._c.pack()
        self._c.bind('<ButtonPress-1>', self.scroll_start)
        self._c.bind('<B1-Motion>', self.scroll_move)

        self.audio_path = audio_path
        self.make_soundboard()

        self.mouse_state = None
        self.pygame = pygame
        self.pygame.init()
        self.pygame.mixer.init(frequency=70000)
        self._w.focus_set()

    @staticmethod
    def get_colour(square, lane):
        colour = square.base_colour
        outline_colour = '#404040'
        if 'breakaway' in square.special:
            rgb = ['0x'+x for x in (
                square.base_colour[1:3],
                square.base_colour[3:5],
                square.base_colour[5:]
            )]
            lighter_rgb = [hex(int(0.5*int(x,16) + 0.5*255)) for x in rgb]
            if lane == 0:
                colour = '#'+''.join(x[2:] for x in lighter_rgb)
            elif lane == 1 and 'breakaway2' in square.special:
                colour = '#'+''.join(x[2:] for x in lighter_rgb)
            elif lane == 2 and 'breakaway3' in square.special:
                colour = '#'+''.join(x[2:] for x in lighter_rgb)
            else:
                colour = square.base_colour

        elif 'divided' in square.special and lane == 1:
            outline_colour = None
            colour = '#83c750'
        elif 'crosswind' in square.special and lane == 0:
            colour = '#dd8833'

        return colour, outline_colour

    def make_soundboard(self):
        self._w.bind("q", self.attaque_de_pierre_rolland)
        self._w.bind("w", lambda event: self.play_audio('hes_racing_on.ogg'))
        self._w.bind("e", lambda event: self.play_audio('fed_up_forming_alliances.ogg'))
        self._w.bind("r", lambda event: self.play_audio('gets_his_head_down.ogg'))
        self._w.bind("t", lambda event: self.play_audio('what_a_finish.ogg'))
        self._w.bind("y", lambda event: self.play_audio('yeeesss_he_takes_it.ogg'))
        self._w.bind("a", lambda event: self.play_audio('nobody_wants_to_chase.ogg'))
        self._w.bind("s", lambda event: self.play_audio('oh_here_we_go_then.ogg'))
        self._w.bind("d", lambda event: self.play_audio('oh_drama_here.ogg'))
        self._w.bind("f", lambda event: self.play_audio('everyone_has_to_be_tired_here.ogg'))
        self._w.bind("g", lambda event: self.play_audio('oh_nightmare_scenario.ogg'))
        self._w.bind("h", lambda event: self.play_audio('oh_heartbreak_here.ogg'))
        self._w.bind("z", lambda event: self.play_audio('absolutely_fantastic.ogg'))
        self._w.bind("x", lambda event: self.play_audio('loved_that.ogg'))
        self._w.bind("c", lambda event: self.play_audio('chuckle.ogg'))
        self._w.bind("v", lambda event: self.play_audio('oh_chapeau_sir.ogg'))

    def activate(self):
        self._w.mainloop()

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
                segment_boundary_geom = np.array([
                    [-0.15, (max(last_width, square.width)/2 + 0.3)*LANE_W],
                    [-0.15, (-max(last_width, square.width)/2 - 0.3)*LANE_W],
                    [0.15, (-max(last_width, square.width)/2 - 0.3)*LANE_W],
                    [0.15, (max(last_width, square.width)/2 + 0.3)*LANE_W]
                ])
                segment_boundary_geom = (segment_boundary_geom @ rotate + position) * SQUARE_SIZE
                segment_boundary_geom[:,-1] *= -1
                colour = last_colour if last_colour != '#777777' else square.base_colour
                segment_boundary = self._c.create_polygon(
                    segment_boundary_geom.flatten().tolist(),
                    fill=colour,
                    outline='#404040',
                    width=(SQUARE_SIZE/10)
                )
                self._c.lift(segment_boundary)
            last_colour = square.base_colour
            last_width = square.width

            if square.curve == 'S':
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
        colour, outline_colour = self.get_colour(square, lane)
        square.spaces[lane] = self._c.create_polygon(
            geometry.flatten().tolist(),
            fill=colour,
            outline=outline_colour,
            width=(SQUARE_SIZE/5)
        )
        if lane*2 - square.width + 3 == 2: self._c.lower(square.spaces[lane])
        func = lambda event: self.click_space(event, square, lane)
        self._c.tag_bind(square.spaces[lane], '<Button-1>', func)
        func = lambda event: self.right_click_space(event, square, lane)
        self._c.tag_bind(square.spaces[lane], '<ButtonPress-3>', func)

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
            self._c.lift(square.text[lane])
            self.mouse_state = None

    def pick_up_rider(self, rider):
        if rider is not None:
            square, lane = rider.position
            square.occupants[lane] = None
            rider._position = None
            colour, _ = self.get_colour(square, lane)
            self._c.itemconfig(square.spaces[lane], fill=colour)
            self._c.delete(square.text[lane])
            self.mouse_state = rider

    def change_background_with_delay(self, colour_sequence):
        self._c.configure(bg=colour_sequence[self.colour_index])
        self.colour_index += 1
        if self.colour_index >= len(colour_sequence):
            return
        else:
            self._w.after(494, lambda: self.change_background_with_delay(colour_sequence))

    def attaque_de_pierre_rolland(self, event):
        self.play_audio('attaque_de_pierre_rolland.ogg')

        self.colour_index = 0
        colour_sequence = ['#ffdd00', '#527439']*7 + ['#ffdd00', '#83c750']

        self._w.after(1270, lambda: self.change_background_with_delay(colour_sequence))

    def play_audio(self, filename):
        self.pygame.mixer.music.load(os.path.join(self.audio_path, filename))
        self.pygame.mixer.music.play()

    def click_space(self, event, square, lane):
        rider = square.occupants[lane]
        if self.mouse_state is None:
            self.pick_up_rider(rider)
        else:
            self.place_rider(self.mouse_state, square, lane)

    def right_click_space(self, event, square, lane):
        rider = square.occupants[lane]
        if rider is not None:
            self.show_rider_information(event, rider)

    def show_rider_information(self, event, rider):
        if rider.team.personalized:
            info = rider.name+'\n'+''.join(str(x) for x in rider.deck)+'\n'+rider.team.name
        else:
            info = rider.name+'\n'+''.join(str(x) for x in rider.deck)+'\n'+rider.__doc__.lstrip()

        text = self._c.create_text(
            self._c.canvasx(event.x),
            self._c.canvasy(event.y),
            text=info,
            font=("Helvetica", 16),
            fill='#000000',
            anchor='sw'
        )
        self._c.bind('<B3-Motion>',
            lambda e: self._c.coords(
                text,
                self._c.canvasx(e.x),
                self._c.canvasy(e.y)
            )
        )
        self._c.bind('<ButtonRelease-3>', lambda e: self._c.delete(text))

    def place_markers(self, annotations):
        for annotation in annotations:
            if annotation == 'S':
                self.place_marker('#33aa00', annotation)
            elif annotation in ('HC', '1', '2', '3', '4'):
                self.place_marker('#cc3333', annotation)
            elif annotation == 'P':
                self.place_marker('#33aa00', annotation)

    def place_marker(self, colour, text=None):
        marker = self._c.create_oval(
            1000, 1000, 1000 + LANE_W*SQUARE_SIZE, 1000 + LANE_W*SQUARE_SIZE,
            fill=colour,
            outline='#404040',
            width=(SQUARE_SIZE/5)
        )
        self._c.lift(marker)

        if text is not None:
            textbox = self._c.create_text(
                1000 + LANE_W*SQUARE_SIZE/2, 1000 + LANE_W*SQUARE_SIZE/2,
                text=text,
                fill='#ffffff',
                tags=marker
            )
            self._c.tag_bind(textbox, '<ButtonPress-1>', lambda e: self.move_marker(e, marker, textbox))
            self._c.tag_bind(textbox, '<Button-3>', lambda e: self.remove_marker(e, marker, textbox))
        else:
            textbox = None
        self._c.tag_bind(marker, '<ButtonPress-1>', lambda e: self.move_marker(e, marker, textbox))
        self._c.tag_bind(marker, '<Button-3>', lambda e: self.remove_marker(e, marker, textbox))

    def move_marker(self, event, marker, textbox):
        def f(e, m, t):
            self._c.coords(
                m,
                self._c.canvasx(e.x) - LANE_W*SQUARE_SIZE/2,
                self._c.canvasy(e.y) - LANE_W*SQUARE_SIZE/2,
                self._c.canvasx(e.x) + LANE_W*SQUARE_SIZE/2,
                self._c.canvasy(e.y) + LANE_W*SQUARE_SIZE/2
            )
            if t is not None:
                self._c.coords(
                    t,
                    self._c.canvasx(e.x),
                    self._c.canvasy(e.y)
                )

        self._c.bind('<B1-Motion>', lambda e:f(e,marker, textbox))
        self._c.bind('<ButtonRelease-1>', lambda event: self._c.bind('<B1-Motion>', self.scroll_move))

    def remove_marker(self, event, marker, textbox):
        self._c.delete(marker)
        if textbox is not None:
            self._c.delete(textbox)

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

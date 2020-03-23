""" Tiles for making courses. """

import numpy as np


BASE_GAME_TILES = dict(
    a='sssss=',
    b='======',
    c='======',
    d='======',
    e='==L',
    f='======',
    g='==L',
    h='==l',
    i='==L',
    j='==R',
    k='==r',
    l='======',
    m='======',
    n='======',
    o='==R',
    p='==R',
    q='==l',
    r='==r',
    s='==r',
    t='==l',
    u='=fffff',

    A='ssss==',
    B='dddd==',
    C='===uuu',
    D='uuuuud',
    E='uuR',
    F='ddd===',
    G='uuR',
    H='ddr',
    I='==R',
    J='==L',
    K='uul',
    L='uuuddd',
    M='==uuuu',
    N='uuuuuu',
    O='uuL',
    P='ddL',
    Q='uur',
    R='uul',
    S='==l',
    T='==r',
    U='uuffff'
)

PELOTON_EXPANSION_TILES = {
    '1': 'SSSSEE',
    '2': 'EEEBE=',
    '3': 'RRRRR=',
    '4': 'RRRRR=',
    '5': 'cCcCcc',
    '6': 'ccCccc',
    '7': '==ccCc',
    '8': '===cCc',
    '9': 'RR=_', #dummy last character

    'v': 'SSSSSE',
    'w': '===b==',
    'x': '==ccCc',
    'y': 'cCcc==',
    'z': 'cc====',
    'V': 'cccCc=',
    'W': 'cCc===',
    'X': 'ccCcc=',
    'Y': 'EE='
}


LANE_W = 1.3
STRAIGHT_L = 2.0
SHARP_R = 3.0
WIDE_R = 5.5
sin45 = (2**0.5)/2
cos45 = sin45
sin22 = ((2 - (2**0.5))**0.5)/2
cos22 = ((2 + (2**0.5))**0.5)/2

GEOMETRIES = dict(
    straight_0=np.array([
        [0, -LANE_W/2],
        [0, -3*LANE_W/2],
        [STRAIGHT_L, -3*LANE_W/2],
        [STRAIGHT_L, -LANE_W/2]
    ]),
    straight_1=np.array([
        [0, 0],
        [0, -LANE_W],
        [STRAIGHT_L, -LANE_W],
        [STRAIGHT_L, 0]
    ]),
    straight_2=np.array([
        [0, LANE_W/2],
        [0, -LANE_W/2],
        [STRAIGHT_L, -LANE_W/2],
        [STRAIGHT_L, LANE_W/2]
    ]),
    straight_3=np.array([
        [0, 0],
        [STRAIGHT_L, 0],
        [STRAIGHT_L, LANE_W],
        [0, LANE_W]
    ]),
    straight_4=np.array([
        [0, 3*LANE_W/2],
        [0, LANE_W/2],
        [STRAIGHT_L, LANE_W/2],
        [STRAIGHT_L, 3*LANE_W/2]
    ]),
    L_1=np.array([
        [0, 0],
        [0, -LANE_W],
        [(SHARP_R+LANE_W)*sin45, SHARP_R-(SHARP_R+LANE_W)*cos45],
        [SHARP_R*sin45, SHARP_R-SHARP_R*cos45]
    ]),
    L_3=np.array([
        [0, 0],
        [SHARP_R*sin45, -SHARP_R*cos45+SHARP_R],
        [(SHARP_R-LANE_W)*sin45, SHARP_R-(SHARP_R-LANE_W)*cos45],
        [0, LANE_W],
    ]),
    R_1=np.array([
        [0, 0],
        [0, -LANE_W],
        [(SHARP_R-LANE_W)*sin45, -(SHARP_R-(SHARP_R-LANE_W)*cos45)],
        [SHARP_R*sin45, SHARP_R*cos45-SHARP_R]
    ]),
    R_3=np.array([
        [0, 0],
        [SHARP_R*sin45, SHARP_R*cos45-SHARP_R],
        [(SHARP_R+LANE_W)*sin45, -(SHARP_R-(SHARP_R+LANE_W)*cos45)],
        [0, LANE_W]
    ]),
    l_1=np.array([
        [0, 0],
        [0, -LANE_W],
        [(WIDE_R+LANE_W)*sin22, WIDE_R-(WIDE_R+LANE_W)*cos22],
        [WIDE_R*sin22, -WIDE_R*cos22+WIDE_R]
    ]),
    l_3=np.array([
        [0, 0],
        [WIDE_R*sin22, -WIDE_R*cos22+WIDE_R],
        [(WIDE_R-LANE_W)*sin22, WIDE_R-(WIDE_R-LANE_W)*cos22],
        [0, LANE_W],
    ]),
    r_1=np.array([
        [0, 0],
        [0, -LANE_W],
        [(WIDE_R-LANE_W)*sin22, -(WIDE_R-(WIDE_R-LANE_W)*cos22)],
        [WIDE_R*sin22, WIDE_R*cos22-WIDE_R]
    ]),
    r_3=np.array([
        [0, 0],
        [WIDE_R*sin22, WIDE_R*cos22-WIDE_R],
        [(WIDE_R+LANE_W)*sin22, -(WIDE_R-(WIDE_R+LANE_W)*cos22)],
        [0, LANE_W]
    ])
)

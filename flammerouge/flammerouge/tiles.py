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
    u='=FFFFF',

    A='ssss==',
    B='DDDD==',
    C='===UUU',
    D='UUUUUD',
    E='UUR',
    F='DDD===',
    G='UUR',
    H='DDr',
    I='==R',
    J='==L',
    K='UUl',
    L='UUUDDD',
    M='==UUUU',
    N='UUUUUU',
    O='UUL',
    P='DDL',
    Q='UUr',
    R='UUl',
    S='==l',
    T='==r',
    U='UUFFFF'
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
    '9': 'RR=_', # dummy last character

    '!': 'SSSSSE',
    '"': '===b==', '@': '===b==',
    '£': '==ccCc',
    '$': 'cCcc==',
    '%': 'cc====',
    '^': 'cccCc=',
    '&': 'cCc===',
    '*': 'ccCcc=',
    '(': 'EE=_' # dummy last character
}

PROMOTIONAL_TILES = {
    '+': '==',
    '-': 'uu'
}

PERSONAL_TILES = {
    'v': 'ddd===',
    'w': 'CCDDDD',
    'x': '=XXXX=',
    'y': 'ddr',
    'z': 'ddR',
    'V': 'dddddd',
    'W': 'ccdddd',
    'X': 'CxxxxC',
    'Y': 'ddl',
    'Z': 'ddL'
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
    L_2=np.array([
        [0, LANE_W/2],
        [0, -LANE_W/2],
        [(SHARP_R+LANE_W/2)*sin45, SHARP_R-(SHARP_R+LANE_W/2)*cos45],
        [(SHARP_R-LANE_W/2)*sin45, SHARP_R-(SHARP_R-LANE_W/2)*cos45]
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
    R_2=np.array([
        [0, LANE_W/2],
        [0, -LANE_W/2],
        [(SHARP_R-LANE_W/2)*sin45, -(SHARP_R-(SHARP_R-LANE_W/2)*cos45)],
        [(SHARP_R+LANE_W/2)*sin45, -(SHARP_R-(SHARP_R+LANE_W/2)*cos45)]
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
    l_2=np.array([
        [0, LANE_W/2],
        [0, -LANE_W/2],
        [(WIDE_R+LANE_W/2)*sin22, WIDE_R-(WIDE_R+LANE_W/2)*cos22],
        [(WIDE_R-LANE_W/2)*sin22, WIDE_R-(WIDE_R-LANE_W/2)*cos22]
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
    r_2=np.array([
        [0, LANE_W/2],
        [0, -LANE_W/2],
        [(WIDE_R-LANE_W/2)*sin22, -(WIDE_R-(WIDE_R-LANE_W/2)*cos22)],
        [(WIDE_R+LANE_W/2)*sin22, -(WIDE_R-(WIDE_R+LANE_W/2)*cos22)]
    ]),
    r_3=np.array([
        [0, 0],
        [WIDE_R*sin22, WIDE_R*cos22-WIDE_R],
        [(WIDE_R+LANE_W)*sin22, -(WIDE_R-(WIDE_R+LANE_W)*cos22)],
        [0, LANE_W]
    ])
)


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

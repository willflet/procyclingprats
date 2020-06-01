""" Tiles for making courses. """

import numpy as np


BASE_GAME_TILES = dict(
    a='sssss=S',
    b='======S',
    c='======S',
    d='======S',
    e='==L',
    f='======S',
    g='==L',
    h='==l',
    i='==L',
    j='==R',
    k='==r',
    l='======S',
    m='======S',
    n='======S',
    o='==R',
    p='==R',
    q='==l',
    r='==r',
    s='==r',
    t='==l',
    u='=FFFFFS',

    A='ssss==S',
    B='DDDD==S',
    C='===UUUS',
    D='UUUUUDS',
    E='UUR',
    F='DDD===S',
    G='UUR',
    H='DDr',
    I='==R',
    J='==L',
    K='UUl',
    L='UUUDDDS',
    M='==UUUUS',
    N='UUUUUUS',
    O='UUL',
    P='DDL',
    Q='UUr',
    R='UUl',
    S='==l',
    T='==r',
    U='UUFFFFS'
)

PELOTON_EXPANSION_TILES = {
    '1': 'SSSSEES',
    '2': 'EEEBE=S',
    '3': 'RRRRR=S',
    '4': 'RRRRR=S',
    '5': 'cCcCccS',
    '6': 'ccCcccS',
    '7': '==ccCcS',
    '8': '===cCcS',
    '9': 'RR=S',

    '!': 'SSSSSES',
    '"': '===b==S', '@': '===b==S',
    '£': '==ccCcS',
    '$': 'cCcc==S',
    '%': 'cc====S',
    '^': 'cccCc=S',
    '&': 'cCc===S',
    '*': 'ccCcc=S',
    '(': 'EE=S'
}

PROMOTIONAL_TILES = {
    '+': '==S',
    '-': 'uuS'
}

PERSONAL_TILES = {
    'v': 'ddd===S',
    'w': 'CCDDDDS',
    'x': '=XXXX=S',
    'y': 'ddr',
    'z': 'ddR',
    'V': 'ddddddS',
    'W': 'ccddddS',
    'X': '=^^^^=S',
    'Y': 'ddl',
    'Z': 'ddL',

    '#': '=rrrr=S',
    '~': 'CxxxxCS',

    '/': '//////S',
    '{': 'RRR',
    '}': 'RRL',
    '[': 'RRr',
    ']': 'RRl',
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
    S_0=np.array([
        [0, -LANE_W/2],
        [0, -3*LANE_W/2],
        [STRAIGHT_L, -3*LANE_W/2],
        [STRAIGHT_L, -LANE_W/2]
    ]),
    S_1=np.array([
        [0, 0],
        [0, -LANE_W],
        [STRAIGHT_L, -LANE_W],
        [STRAIGHT_L, 0]
    ]),
    S_2=np.array([
        [0, LANE_W/2],
        [0, -LANE_W/2],
        [STRAIGHT_L, -LANE_W/2],
        [STRAIGHT_L, LANE_W/2]
    ]),
    S_3=np.array([
        [0, LANE_W],
        [0, 0],
        [STRAIGHT_L, 0],
        [STRAIGHT_L, LANE_W]
    ]),
    S_4=np.array([
        [0, 3*LANE_W/2],
        [0, LANE_W/2],
        [STRAIGHT_L, LANE_W/2],
        [STRAIGHT_L, 3*LANE_W/2]
    ]),
    L_0=np.array([
        [0, -LANE_W/2],
        [0, -3*LANE_W/2],
        [(SHARP_R+3*LANE_W/2)*sin45, SHARP_R-(SHARP_R+3*LANE_W/2)*cos45],
        [(SHARP_R+LANE_W/2)*sin45, SHARP_R-(SHARP_R+LANE_W/2)*cos45]
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
        [0, LANE_W],
        [0, 0],
        [SHARP_R*sin45, -SHARP_R*cos45+SHARP_R],
        [(SHARP_R-LANE_W)*sin45, SHARP_R-(SHARP_R-LANE_W)*cos45]
    ]),
    L_4=np.array([
        [0, 3*LANE_W/2],
        [0, LANE_W/2],
        [(SHARP_R-LANE_W/2)*sin45, SHARP_R-(SHARP_R-LANE_W/2)*cos45],
        [(SHARP_R-3*LANE_W/2)*sin45, SHARP_R-(SHARP_R-3*LANE_W/2)*cos45]
    ]),
    R_0=np.array([
        [0, -LANE_W/2],
        [0, -3*LANE_W/2],
        [(SHARP_R-3*LANE_W/2)*sin45, -(SHARP_R-(SHARP_R-3*LANE_W/2)*cos45)],
        [(SHARP_R-LANE_W/2)*sin45, -(SHARP_R-(SHARP_R-LANE_W/2)*cos45)]
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
        [0, LANE_W],
        [0, 0],
        [SHARP_R*sin45, SHARP_R*cos45-SHARP_R],
        [(SHARP_R+LANE_W)*sin45, -(SHARP_R-(SHARP_R+LANE_W)*cos45)]
    ]),
    R_4=np.array([
        [0, 3*LANE_W/2],
        [0, LANE_W/2],
        [(SHARP_R+LANE_W/2)*sin45, -(SHARP_R-(SHARP_R+LANE_W/2)*cos45)],
        [(SHARP_R+3*LANE_W/2)*sin45, -(SHARP_R-(SHARP_R+3*LANE_W/2)*cos45)],
    ]),
    l_0=np.array([
        [0, -LANE_W/2],
        [0, -3*LANE_W/2],
        [(WIDE_R+3*LANE_W/2)*sin22, WIDE_R-(WIDE_R+3*LANE_W/2)*cos22],
        [(WIDE_R+LANE_W/2)*sin22, WIDE_R-(WIDE_R+LANE_W/2)*cos22]
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
        [0, LANE_W],
        [0, 0],
        [WIDE_R*sin22, -WIDE_R*cos22+WIDE_R],
        [(WIDE_R-LANE_W)*sin22, WIDE_R-(WIDE_R-LANE_W)*cos22]
    ]),
    l_4=np.array([
        [0, 3*LANE_W/2],
        [0, LANE_W/2],
        [(WIDE_R-LANE_W/2)*sin22, WIDE_R-(WIDE_R-LANE_W/2)*cos22],
        [(WIDE_R-3*LANE_W/2)*sin22, WIDE_R-(WIDE_R-3*LANE_W/2)*cos22]
    ]),
    r_0=np.array([
        [0, -LANE_W/2],
        [0, -3*LANE_W/2],
        [(WIDE_R-3*LANE_W/2)*sin22, -(WIDE_R-(WIDE_R-3*LANE_W/2)*cos22)],
        [(WIDE_R-LANE_W/2)*sin22, -(WIDE_R-(WIDE_R-LANE_W/2)*cos22)]
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
        [0, LANE_W],
        [0, 0],
        [WIDE_R*sin22, WIDE_R*cos22-WIDE_R],
        [(WIDE_R+LANE_W)*sin22, -(WIDE_R-(WIDE_R+LANE_W)*cos22)]
    ]),
    r_4=np.array([
        [0, 3*LANE_W/2],
        [0, LANE_W/2],
        [(WIDE_R+LANE_W/2)*sin22, -(WIDE_R-(WIDE_R+LANE_W/2)*cos22)],
        [(WIDE_R+3*LANE_W/2)*sin22, -(WIDE_R-(WIDE_R+3*LANE_W/2)*cos22)],
    ]),
)

""" Tiles for making courses. """

import numpy as np


BASE_GAME_TILES = dict(
    a='[[[[[=|',
    b='======|',
    c='======|',
    d='======|',
    e='==>',
    f='======|',
    g='==>',
    h='==)',
    i='==>',
    j='==<',
    k='==(',
    l='======|',
    m='======|',
    n='======|',
    o='==<',
    p='==<',
    q='==)',
    r='==(',
    s='==(',
    t='==)',
    u='=]]]]]|',

    A='[[[[==|',
    B='VVVV==|',
    C='===AAA|',
    D='AAAAAV|',
    E='AA<',
    F='VVV===|',
    G='AA<',
    H='VV(',
    I='==<',
    J='==>',
    K='AA)',
    L='AAAVVV|',
    M='==AAAA|',
    N='AAAAAA|',
    O='AA>',
    P='VV>',
    Q='AA(',
    R='AA)',
    S='==)',
    T='==(',
    U='AA]]]]|'
)

PELOTON_EXPANSION_TILES = {
    '1': '{{{{++|',
    '2': '+++B+=|',
    '3': 'FFFFF=|',
    '4': 'FFFFF=|',
    '5': 'cCcCcc|',
    '6': 'ccCccc|',
    '7': '==ccCc|',
    '8': '===cCc|',
    '9': 'FF=|',

    '!': '{{{{{+|',
    '"': '===b==|', '@': '===b==|',
    '£': '==ccCc|',
    '$': 'cCcc==|',
    '%': 'cc====|',
    '^': 'cccCc=|',
    '&': 'cCc===|',
    '*': 'ccCcc=|',
    '(': '++=|'
}

PROMOTIONAL_TILES = {
    '+': '==|',
    '-': 'aa|'
}

PERSONAL_TILES = {
    'v': 'vvv===|',
    'w': 'CCVVVV|',
    'x': '=::::=|',
    'y': 'vv(',
    'z': 'vv<',
    'V': 'vvvvvv|',
    'W': 'ccvvvv|',
    'X': '=mmmm=|',
    'Y': 'vv)',
    'Z': 'vv>',

    '#': '=ffff=|',
    '~': 'CggggC|',

    '/': 'XXXXXX|',
    '{': 'FF<',
    '}': 'FF>',
    '[': 'FF(',
    ']': 'FF)',
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

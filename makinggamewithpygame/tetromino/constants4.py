import pygame, sys, random, time, copy
from pygame.locals import *
from pygame import Color as pyColor
from rotateXY import rotate90

fps = 25 
screenwidth,screenheight = 800,600
boxsize = 25 
boardwidth,boardheight= 10,20
blank = '.'

up,down,left,right = 'up','down','left','right'

xmargin = (screenwidth - boardwidth * boxsize) /2
topmargin = screenheight - boardheight * boxsize - 5

#  R G B
gray = pyColor('gray')
black = pyColor('black')
c1 = white,red,blue,green,yellow \
   = pyColor('white'),pyColor('red'),\
     pyColor('blue'),pyColor('green'),pyColor('yellow')
c2 = skyblue,steelblue,royalblue,cyan \
   = pyColor('skyblue'),pyColor('steelblue'),pyColor('royalblue'),pyColor('cyan')
c3 = purple,orange,pink \
   = pyColor('purple'),pyColor('orange'),pyColor('pink')
c4 = khaki,yellowgreen \
   = pyColor('khaki'), pyColor('yellowgreen')
colors = [ color for color in c1+c2+c3+c4]

bordercolor = 40,40,40 #blue #20,20,20 #blue
bordercolor2 = 15,15,15 #blue
gridcolor = bordercolor2
bgcolor   = black
textcolor = white
textshadowcolor = gray
boardbgcolor = bgcolor #20,20,20 
#gridcolor = boardbgcolor[0]+40,boardbgcolor[1]+40, boardbgcolor[2]+ 40
#gridcolor2 = boardbgcolor[0]+50,boardbgcolor[1]+50, boardbgcolor[2]+50

#------------------ tetris shapes ---------------------

tetrisS = [
    list(  '.....' ),
    list(  '..OO.' ),
    list(  '.OO..' ),
    list(  '.....' )
   ]

tetrisZ = [
    list( '.....' ),
    list( '.OO..' ),
    list( '..OO.' ),
    list( '.....' )
]

tetrisI = [
    list( '..O..' ),
    list( '..O..' ),
    list( '..O..' ),
    list( '..O..' ),
]

tetrisO = [
    list( '.....' ),
    list( '.OO..' ),
    list( '.OO..' ),
    list( '.....' )
]

tetrisJ = [
    list( '.....' ),
    list( '.O...' ),
    list( '.OOO.' ),
    list( '.....' ),
]

tetrisL = [
    list( '.....' ),
    list( '...O.' ),
    list( '.OOO.' ),
    list( '.....' )
]

tetrisT = [
    list( '.....' ),
    list( '..O..' ),
    list( '.OOO.' ),
    list( '.....' ),
]

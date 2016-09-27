import pygame, sys, random,time, math
from pygame.locals import *

fps = 30
winwidth,winheight = 640,480
glasscolor = 24,255,0
white = 255,255,255
red = 255,0,0

cameraslack = 90 # how far from the center the squirrel moves before moving the screen
moverate = 9 # how fast the player moves
bouncerate = 6 # how fast the player bounces(large is slower)
bounceheight = 30 # how high the player bounces
startsize = 25 # how big the player starts off
winsize =300 # how big the player needs to be to win
invulntime = 2 # how long the player is invulnerable after hit in seconds
gameovertime = 4 # how long the 'game over' text stays on the screen in seconds
maxhealth = 3 # how much health the player starts with

numgrass = 80 # number of grass objects in the active area
numsquirrels = 30 # number of squirrels in the active area
squirrelminspeed = 3 # slowest squirrel spped
squirrelmaxspeed = 7 # fastest squirrel speed
dirchangefreq = 2 # %chance of direction change per frame
left,right = 'left','right'

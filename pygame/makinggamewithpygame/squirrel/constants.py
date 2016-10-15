import pygame, sys, random,time, math
from pygame.locals import *

fps = 30
#winwidth,winheight = 320,200
winwidth,winheight = 640,480
#winwidth,winheight = 800,600
grasscolor = 24,255,0
white = 255,255,255
red = 255,0,0

cameraslack = 30#90 # how far from the center the squirrel moves before moving the screen
moverate = 9 # how fast the player moves
bouncerate = 6 # how fast the player bounces(large is slower)
bounceheight = 30 # how high the player bounces
startsize = 20 # how big the player starts off
winsize = 100 # how big the player needs to be to win
invulntime = 2 # how long the player is invulnerable after hit in seconds
gameovertime = 4 # how long the 'game over' text stays on the screen in seconds
maxhealth = 3 # how much health the player starts with

numgrass = 80 # number of grass objects in the active area
numsquirrels = 30 # number of squirrels in the active area
squirrelminspeed = 1#3 # slowest squirrel spped
squirrelmaxspeed = 5#7 # fastest squirrel speed
dirchangefreq = 2 # %chance of direction change per frame
left,right = 'left','right'

l_squir_img = pygame.image.load('squirrel.png')
r_squir_img = pygame.transform.flip(l_squir_img,True, False)
l_player_img = pygame.image.load('player.png')
r_player_img = pygame.transform.flip(l_player_img,True, False)

'''
this program has three data structures to represent the player, enemy squirrels, and grass background objects.
the data structures are dictionaries with the following keys.
keys used by all three data structures:
    'x' - the left edge coordinate of the object in the game world(not a pixel coordinate)
    'y' - the top edge coordinate of the object in the game world(not a pixel coordinate)
    'rect' - the pygame.Rect object representing where on the screen the object is located.
player data structure keys:
    'surface' - the pygame.Surface object that stores the image of the squirrel which will be drawn to the screen
    'facing' - either set to LEFT or RIGHT, stores which direction the player is facing
    'size' - the width and height of the player in pixels
    'bouce' - represents at what point in a bounce the player is in. 0 means standing(no bounce), up to bounceRate
enemy squirrel data structure keys:
    'surface' - the pygame.Surface object that stores the image of the squirrel which will be drawn to the screen
    'movex' - how many pixels per frame the squireel moves horizontally. a negative integer is moving to the left
              a positive to the right
    'movey' - how many pixels per frame the squirrel moves vertically. a negative integer is moving up, a positive
              moving down
    'width' - the width of the squirrel's image, in pixels
    'height' - the height of the squirrel's image, in pixels
    'bounce' - represents at what point in a bounce the player is in. 0 means standing(no bounce), up to bounceRate
    'bounceRate' - how quickly the squirrel bounces. a lower number means a quicker bounce.
    'bounceheight' - how high the squirrel bounces
    'grassImage' - an integer that refers to the index of the pygame.Surface object in grassImages used for this 
                   grass object
'''

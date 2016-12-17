import pygame,os,sys
sys.path.append('..')
from random import randint,choice
from math import sin,cos,radians
from gridmap import GridMap
from pathfinder import PathFinder
from simpleanimation import SimpleAnimation
from utils import Timer
from vec2d import vec2d
from widgets import Box, MessageBoard

# images
BG_TITLE_IMG = '../images/brick_tile.png'
SCREEN_WIDTH, SCREEN_HEIGHT = 580, 500
GRID_SIZE = 20
FIELD_SIZE = 400,400
CREEP_FILENAMES = [
        ('../images/bluecreep_0.png', '../images/bluecreep_45.png'),
        ('../images/greencreep_0.png', '../images/greencreep_45.png'),
        ('../images/yellowcreep_0.png', '../images/yellowcreep_45.png'),
        ('../images/pinkcreep_0.png', '../images/pinkcreep_45.png'),
        ]
MAX_N_CREEPS = 50

# colors
red = pygame.Color('red')
green = pygame.Color('green')
yellow = pygame.Color('yellow')
black = pygame.Color('black')
white = pygame.Color('white')
gray = pygame.Color('gray')
darkgray = pygame.Color('darkgray')

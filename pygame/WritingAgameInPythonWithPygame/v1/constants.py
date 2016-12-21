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
#SCREEN_WIDTH, SCREEN_HEIGHT = 580, 500
#GRID_SIZE = 20
#FIELD_SIZE = 400,400
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 40
FIELD_SIZE = 600,600
CREEP_FILENAMES = [
        ('../images/bluecreep_0.png', '../images/bluecreep_45.png'),
        ('../images/greencreep_0.png', '../images/greencreep_45.png'),
        ('../images/yellowcreep_0.png', '../images/yellowcreep_45.png'),
        ('../images/pinkcreep_0.png', '../images/pinkcreep_45.png'),
        ]
imgs = ('../images/greencreep_0.png', '../images/greencreep_45.png')
wall_img = pygame.image.load(BG_TITLE_IMG)
wall_img = pygame.transform.scale(wall_img,(GRID_SIZE,GRID_SIZE) )
creep_imgs = [ pygame.image.load(img) for img in imgs ]
explosion_img = pygame.image.load('../images/explosion1.png')#.convert_alpha()
MAX_N_CREEPS = 50

# colors
red = pygame.Color('red')
green = pygame.Color('green')
yellow = pygame.Color('yellow')
black = pygame.Color('black')
white = pygame.Color('white')
gray = pygame.Color('gray')
darkgray = pygame.Color('darkgray')


if __name__ == '__main__':
#   tile = pygame.transform.scale(wall_img,(50,50) )
    print wall_img.get_size()

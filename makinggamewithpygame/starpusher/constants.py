import pygame, sys, random, os, copy
from pygame.locals import *
fps = 30
winwidth,winheight = 800,600
wincenter = halfwinwidth,halfwinheight = winwidth/2,winheight/2
# total width and height of each tile in pixels
tilewidth = 50
tileheight = 85
tilefloorheight = 45

camspeed = 5 # how many pixels per frame the camera moves
# the percentage of outdoor titles that have additional decoration
# on them such as tree or rock
outside_decoration_pct = 20
brightblue = 0,170,255
white = 255,255,255
bgcolor = brightblue
textcolor = white

up,down,left,right = 'up','down','left','right'

pygame.init()
fpsclock = pygame.time.Clock()
displaysurf = pygame.display.set_mode( (winwidth,winheight))
pygame.display.set_caption('Star Pusher')
basicfont = pygame.font.Font('freesansbold.ttf',18)
# a global dict value that will contain all the pygame suface objects returned by
# pygame.image.load()
class images:
    uncoveredgoal =  pygame.image.load('RedSelector.png')
    coveredgoal  =  pygame.image.load('Selector.png')
    star          =  pygame.image.load('Star.png')
    corner        =  pygame.image.load('Wall_Block_Tall.png')
    wall          =  pygame.image.load('Wood_Block_Tall.png')
    insidefloor   =  pygame.image.load('Plain_Block.png')
    outsidefloor  =  pygame.image.load('Grass_Block.png')
    title         =  pygame.image.load('star_title.png')
    solved        =  pygame.image.load('star_solved.png')
    princess      =  pygame.image.load('princess.png')
    boy           =  pygame.image.load('boy.png')
    catgirl       =  pygame.image.load('catgirl.png')
    horngirl      =  pygame.image.load('horngirl.png')
    pinkgirl      =  pygame.image.load('pinkgirl.png')
    rock          =  pygame.image.load('Rock.png')
    shorttree     =  pygame.image.load('Tree_Short.png')
    talltree      =  pygame.image.load('Tree_Tall.png')
    uglytree      =  pygame.image.load('Tree_Ugly.png')
# these dict values are global, and map the character that appears in the level file
# to the surface object it represents


tilemapping = {'x':images.corner,
                '#':images.wall,
                'o':images.insidefloor,
                ' ':images.outsidefloor }
outsidedecomapping = {'1':images.rock,
                      '2':images.shorttree,
                      '3':images.talltree,
                      '4':images.uglytree }
currentimage = 0
playerimages = [images.princess,images.boy,images.catgirl,images.horngirl,images.pinkgirl ]
currentlevelindex = 0

if __name__ == '__main__':
    print images
    print images.title
    x = images.title
    print x.get_rect()
    print images.title.get_rect()

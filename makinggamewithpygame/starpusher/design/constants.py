import pygame,sys,random,os,copy
from pygame.locals import *

fps = 15 #30
winwidth,winheight = 800,600
wincenter = halfwinwidth,halfwinheight = winwidth/2,winheight/2
tilewidth,tileheight = 50,85 #50,85
tilefloorheight = 40

# the percentage of outdoor titles that have additional decoration on them such as tree or rock
outside_decoration_pct = 20
# R G B
white = pygame.Color('white')
black = pygame.Color('black')
gray = pygame.Color('gray')
yellow = pygame.Color('yellow')
pink = pygame.Color('pink')
red = pygame.Color('red')
green = pygame.Color('green')
darkgreen = pygame.Color('darkgreen')
brightblue = 0, 170, 255
bgcolor = brightblue
textcolor = white
up,down,left,right = 'up','down','left','right'

pygame.init()
fpsclock = pygame.time.Clock()
displaysurf = pygame.display.set_mode( (winwidth,winheight))
pygame.display.set_caption('Star Pusher')
basicfont = pygame.font.Font('freesansbold.ttf',18)

# a global dict value that will contain all the pygame suface objects returned by
class images:
    uncoveredgoal =  pygame.image.load('..\\images\\RedSelector.png')
    coveredgoal   =  pygame.image.load('..\\images\\Selector.png')
    star          =  pygame.image.load('..\\images\\Star.png')
    corner        =  pygame.image.load('..\\images\\Wall_Block_Tall.png')
    wall          =  pygame.image.load('..\\images\\Wood_Block_Tall.png')
    insidefloor   =  pygame.image.load('..\\images\\Plain_Block.png')
    outsidefloor  =  pygame.image.load('..\\images\\Grass_Block.png')
    title         =  pygame.image.load('..\\images\\star_title.png')
    solved        =  pygame.image.load('..\\images\\star_solved.png')
    princess      =  pygame.image.load('..\\images\\princess.png')
    boy           =  pygame.image.load('..\\images\\boy.png')
    catgirl       =  pygame.image.load('..\\images\\catgirl.png')
    horngirl      =  pygame.image.load('..\\images\\horngirl.png')
    pinkgirl      =  pygame.image.load('..\\images\\pinkgirl.png')
    rock          =  pygame.image.load('..\\images\\Rock.png')
    shorttree     =  pygame.image.load('..\\images\\Tree_Short.png')
    talltree      =  pygame.image.load('..\\images\\Tree_Tall.png')
    uglytree      =  pygame.image.load('..\\images\\Tree_Ugly.png')
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
currentlevelindex = 0

if __name__ == '__main__':
    surf =  images.title
    rect = surf.get_rect()
    displaysurf.blit(surf,rect)
    while True:
        for e in pygame.event.get():
            if e.type == QUIT: pygame.quit(); sys.exit()
        pygame.display.update()

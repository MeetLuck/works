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
SCREEN_WIDTH, SCREEN_HEIGHT = 800,800#, 600
GRID_SIZE = 60
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


class GameHelper(object):

    def getTboard(self,text):
        self.tboard_text = [text]
        self.tboard_rect = pygame.Rect(20, 20, self.field_outer_width, 30)
        self.tboard_bgcolor = pygame.Color(50, 20, 0)
        return MessageBoard(self.screen,
            rect=self.tboard_rect,
            bgcolor=self.tboard_bgcolor,
            border_width=4,
            border_color=black,
            text=self.tboard_text,
            font=('tahoma', 18),
            font_color=yellow)

    def getFieldBox(self):
        self.field_border_width = 4 
        self.field_outer_width  = FIELD_SIZE[0] + 2 * self.field_border_width
        self.field_outer_height = FIELD_SIZE[1] + 2 * self.field_border_width
        self.field_rect_outer = pygame.Rect(20,60, self.field_outer_width, self.field_outer_height)
        self.field_bgcolor = pygame.Color(109,41,1,100)
        self.field_border_color = black
        return Box(self.screen, rect=self.field_rect_outer, bgcolor= self.field_border_width,
                border_color = self.field_border_color)
    def createWalls(self):
        walls_list = list()
        for r in range(0,9):
            walls_list.append( (r,6) )
            if r != 7:
                walls_list.append( (r,3) )
                walls_list.append( (r,4) )
            if r > 4:
                walls_list.append( (r,1) )
        for r in range(4,10):
            walls_list.append( (r,8) )
        self.walls = dict().fromkeys(walls_list,True)
    def drawPostals(self):
        self.entrance_rect = pygame.Rect(self.field_rect.left, self.field_rect.top,
                                         2*GRID_SIZE,2*GRID_SIZE)
        self.exit_rect = pygame.Rect(self.field_rect.right - 2*GRID_SIZE,
                                     self.field_rect.bottom - 2*GRID_SIZE,
                                     2*GRID_SIZE, 2*GRID_SIZE)
        entrance = pygame.Surface( (self.entrance_rect.w, self.entrance_rect.h) )
        entrance.fill(pygame.Color(80,200,80) )
        entrance.set_alpha(150)
        self.screen.blit(entrance,self.entrance_rect)
        exit = pygame.Surface( (self.exit_rect.w,self.exit_rect.h) )
        exit.fill( pygame.Color(200,80,80) )
        exit.set_alpha(150)
        self.screen.blit(exit,self.exit_rect)

    def drawGrid(self):
        for y in range(self.grid_nrows+1):
            pygame.draw.line(self.screen, pygame.Color(50,50,50),
                    (self.field_rect.left, self.field_rect.top+y*GRID_SIZE-1),
                    (self.field_rect.right, self.field_rect.top + y*GRID_SIZE-1) )
        for x in range(self.grid_ncols+1):
            pygame.draw.line(self.screen,pygame.Color(50,50,50),
                    (self.field_rect.left + x*GRID_SIZE-1,self.field_rect.top),
                    (self.field_rect.left + x*GRID_SIZE-1,self.field_rect.bottom-1) )
    def drawWalls(self):
        rect = wall_img.get_rect()
        for wall in self.walls:
            rect.center = self.coordToScreenPos(wall)
            self.screen.blit(wall_img,rect)

if __name__ == '__main__':
#   tile = pygame.transform.scale(wall_img,(50,50) )
    print wall_img.get_size()

# 017 turning and physics.py
# move the BIG bird around with W,A,S,D and Q and E
# fire with SPACE, toggle gravity with G

import pygame,random,os
from math import pi,sin,cos,atan2
from colors import *

pygame.mixer.pre_init(44100,-16,2,2048)
pygame.init()
screensize = screenwidth,screenheight = 640,480
screen = pygame.display.set_mode( screensize )
screenrect = screen.get_rect()
clock = pygame.time.Clock()
fps = 6
#fps = 60
folder = 'data'

def write(msg='pygame is cool',color=darkblue):
    font = pygame.font.SysFont('None',20)
    textsurf = font.render(msg,True,color)
    textsurf = textsurf.convert_alpha()
    return textsurf

class  Target:

    def __init__(self,bgsurf):
        self.width,self.height = 200,100
        #self.width,self.height = 100,200#,50
        self.angle = 0.0
        self.center = screenwidth/2,screenheight/2
        self.reset()
    def reset(self):
        self.surf = pygame.Surface( (self.width,self.height) )
        self.surf.set_colorkey(black)
        #self.surf.fill(green)
        self.rect = self.surf.get_rect()
        pygame.draw.rect(self.surf,blue,self.rect,1)
        leftrect = 1,1,10,10
        rightrect = self.rect.right-10-1,self.rect.top+1,10,10
        horizontal_halfrect = 0,0,self.rect.width,self.rect.height/2
        vertical_halfrect = 0,0,self.rect.width/2,self.rect.height
        pygame.draw.rect(self.surf,red,leftrect)
        pygame.draw.rect(self.surf,green,rightrect)
        pygame.draw.line(self.surf,red,self.rect.midtop,self.rect.midbottom,1)
        pygame.draw.line(self.surf,red,self.rect.midleft,self.rect.midright,2)
        pygame.draw.circle(self.surf,red,self.rect.center,10,2)
        self.surf = self.surf.convert_alpha()
        self.orisurf = self.surf.copy()
        self.setCenter()
    def setCenter(self):
        self.rect.center = self.center
    def draw(self):
        bgsurf.blit( write(str(t.rect)) ,(20,40) )
        bgsurf.blit( write('center = ' + str(t.rect.center)), (20,60) )
        bgsurf.blit( write('angle = '  + str(self.angle)),    (20,80) )
        #bgsurf.blit( write(str(self.angle%360)) ,(20,80) )
        bgsurf.blit(self.surf, self.rect.topleft)

        #pygame.draw.rect(self.surf,green,(0,0,
    def rotate(self,key):
        if key == pygame.K_a: # turn left, counter-clockwise
            self.angle += +15 #self.rotatespeed
        if key == pygame.K_d: # turn right, clockwise
            self.angle += -15 #self.rotatespeed
        print self.angle
        if self.angle > 360:
            self.angle += -360
        elif self.angle < -360:
            self.angle += 360
#       self.surf = rot_center(self.surf,self.angle)
        self.surf = pygame.transform.rotate(self.orisurf, self.angle)
        self.rect = self.surf.get_rect(center = self.center)
        bgsurf.blit(self.surf, self.rect.topleft)
        #pygame.draw.rect(rotsurf, red, rotrect,3)
        self.draw()
        #self.setCenter()

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def rot_center(image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect


darkness = 0.85
bgcolor = darkness*white[0], darkness*white[0], darkness*white[0]

# ----------------- background artwork -------------  
bgsurf = pygame.Surface((screen.get_width(), screen.get_height()))
bgsurf.fill(bgcolor)     # fill white
bgsurf = bgsurf.convert()  # jpg can not have transparency

#playersurf = pygame.Surface( (100,100) )
t = Target(bgsurf)
#t.draw(bgsurf)
mainloop = True
while mainloop:
    for e in pygame.event.get():
        if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            mainloop = False
        if e.type == pygame.KEYDOWN:
            t.rotate(e.key)
    #print t.rect.center
    bgsurf.fill(bgcolor)
    pygame.draw.line(bgsurf,black,screenrect.midleft,screenrect.midright,1)
    pygame.draw.line(bgsurf,black,screenrect.midtop,screenrect.midbottom,1)
    pygame.draw.circle(bgsurf,darkgray,(screenwidth/2,screenheight/2), 100,1)
    pygame.draw.circle(bgsurf,gray,(screenwidth/2,screenheight/2), 200,1)
    t.draw()
    screen.blit(bgsurf, (0,0))     # blit background on screen (overwriting all)
    pygame.display.flip()
    clock.tick(fps)


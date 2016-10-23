# 017 turning and physics.py
# move the BIG bird around with W,A,S,D and Q and E
# fire with SPACE, toggle gravity with G

import pygame,random,os
from math import pi,sin,cos,atan2,sqrt
from colors import *
GRAD =  2*pi/360

pygame.mixer.pre_init(44100,-16,2,2048)
pygame.init()
screensize = screenwidth,screenheight = 800,600 #640,480
screen = pygame.display.set_mode( screensize )
screenrect = screen.get_rect()
clock = pygame.time.Clock()
fps = 6
direction = None
#fps = 60
folder = 'data'

def write(msg='pygame is cool',color=darkblue):
    font = pygame.font.SysFont('Arial bold',20)
    textsurf = font.render(msg,True,color)
    textsurf = textsurf.convert_alpha()
    return textsurf

def drawTracks():
    pygame.draw.line(bgsurf,black,screenrect.midleft,screenrect.midright,1)
    pygame.draw.line(bgsurf,black,screenrect.midtop,screenrect.midbottom,1)
    pygame.draw.circle(bgsurf,darkgray,screenrect.center,100,1)
    pygame.draw.circle(bgsurf,gray,screenrect.center,200,1)
    pygame.draw.circle(bgsurf,gray,screenrect.center,300,1)

class Car:
    def __init__(self):
        self.width,self.height = 50,100
        self.angle = 0.0
        self.speed = 1.0
        # going forward(north)
        self.dirx = 0.0
        self.diry = 0.0
        self.makeCar()
    def makeCar(self):
        self.surf = pygame.Surface( (self.width,self.height) )
        #self.surf.set_colorkey(black)
        self.surf.fill(darkgray)
        self.rect = self.surf.get_rect()
        # draw frame
        framerect = 1,1,self.rect.width-1,self.rect.height-1
        pygame.draw.rect(self.surf,blue,framerect,1)
        # draw front lights
        left_light= 10,10
        right_light = self.rect.right-10,self.rect.top+10
        # left light
        pygame.draw.circle(self.surf,yellow,left_light,10)
        pygame.draw.circle(self.surf,green,left_light,8,2)
        # right light
        pygame.draw.circle(self.surf,yellow,right_light,10)
        pygame.draw.circle(self.surf,green,right_light,8,2)
        # mid lines
        pygame.draw.line(self.surf,black,self.rect.midtop,self.rect.midbottom,1)
        pygame.draw.line(self.surf,black,self.rect.midleft,self.rect.midright,1)
        # origin
        pygame.draw.circle(self.surf,red,self.rect.center,10,2)
        self.surf = self.surf.convert_alpha()
        self.orisurf = self.surf.copy()
        self.setCenter()
    def setCenter(self):
        self.rect.center = screenrect.center
        # we need x,y to move self.rect.center because self.rect.center is ALWAYS INT type.
        self.x,self.y = self.rect.center
    def draw(self):
        bgsurf.blit( write(str(self.rect)) ,(20,40) )
        bgsurf.blit( write('center = ' + str(self.rect.center)), (20,60) )
        bgsurf.blit( write('angle = '  + str(self.angle)),    (20,80) )
        bgsurf.blit( write('speed = %.2f' %self.speed, purple),    (20,100) )
        #bgsurf.blit( write(str(self.angle%360)) ,(20,80) )
        bgsurf.blit(self.surf, self.rect)
        #pygame.draw.rect(self.surf,green,(0,0,
    def speedUp(self):
        self.speed *= 1.05
    def speedDown(self):
        self.speed *= 0.90 
    def setSpeed(self,key):
        if key == pygame.K_k:
            #print 'k pressed, SpeedUp'
            self.speedUp()
        elif key == pygame.K_SPACE:
            #print 'j pressed, BREAK'
            self.speedDown()
    def move(self):
        # set direction, moving forward
        self.dirx = -sin(self.angle*GRAD) 
        self.diry = -cos(self.angle*GRAD)
        # set speed
        self.dx = self.dirx * self.speed
        self.dy = self.diry * self.speed
        # move surface
        self.x += self.dx
        self.y += self.dy
        self.rect.center = self.x,self.y
        #print 'speed =>',self.speed,self.dx,self.dy
        #print 'location =>',self.x,self.y, self.rect.center

    def turn(self,key):
        if key == pygame.K_h: # turn left, counter-clockwise
            self.angle += +5 #self.rotatespeed
        elif key == pygame.K_l: # turn right, clockwise
            self.angle += -5 #self.rotatespeed
        else:
            return
        #print self.angle
        if self.angle > 360:
            self.angle += -360
        elif self.angle < -360:
            self.angle += 360
#        self.surf = rot_center(self.surf,self.angle)
        self.surf = pygame.transform.rotate(self.orisurf, self.angle)
        self.rect = self.surf.get_rect(center= self.rect.center)
        #self.setCenter()
        bgsurf.blit(self.surf, self.rect)
        #pygame.draw.rect(rotsurf, red, rotrect,3)
        self.draw()
        #self.setCenter()

darkness = 0.85
bgcolor = darkness*white[0], darkness*white[0], darkness*white[0]

# ----------------- background -------------  
bgsurf = pygame.Surface((screen.get_width(), screen.get_height()))
bgsurf.fill(bgcolor)     
bgsurf = bgsurf.convert()

#playersurf = pygame.Surface( (100,100) )
car = Car()
#t.draw(bgsurf)
mainloop = True
while mainloop:
    for e in pygame.event.get():
        if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            mainloop = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_h or e.key == pygame.K_l:
                car.turn(e.key)
            elif e.key == pygame.K_k or e.key == pygame.K_SPACE:
                car.setSpeed(e.key)
    car.move()
    #print t.rect.center
    bgsurf.fill(bgcolor)
    drawTracks()
    car.draw()
    screen.blit(bgsurf, (0,0))     # blit background on screen (overwriting all)
    pygame.display.flip()
    clock.tick(fps)


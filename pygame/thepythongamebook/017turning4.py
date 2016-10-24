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
#fps = 6
direction = None
fps = 60
folder = 'data'

def write(msg='pygame is cool',color=darkblue):
    font = pygame.font.SysFont('Arial bold',20)
    textsurf = font.render(msg,True,color)
    textsurf = textsurf.convert_alpha()
    return textsurf

def drawTracks():
    for angle in range(0,360,15):
        grad = 2*pi/360.0
        dirx = -sin(angle*grad)
        diry = -cos(angle*grad)
        dest = screenrect.centerx + dirx*200,screenrect.centery+diry*200
        dest = int(dest[0]),int(dest[1])
        #print angle, dirx,diry, dest
        pygame.draw.line(bgsurf,darkgray,screenrect.center,dest,1)
        pygame.draw.circle(bgsurf,purple,dest,2)
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
        self.start = False
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
        # arrow indicating moving direction
        w,h = self.rect.size
        cx,cy = self.rect.center
        arrowcolor = purple
        pointlist = self.rect.midtop, (cx-w/4,cy-h/8),(cx+w/4,cy-h/8),self.rect.midtop
        #print pointlist
        pygame.draw.polygon(self.surf,arrowcolor,pointlist)
        #arrowrect = self.rect.midtop[0]-w/2,self.rect.midtop[1],w,self.height
        arrowrect = cx-w/8,cy-h/4,w/4,h/2+h/4
        pygame.draw.rect(self.surf,arrowcolor ,arrowrect)
        # mid cross lines
        pygame.draw.line(self.surf,black,self.rect.midtop,self.rect.midbottom,1)
        pygame.draw.line(self.surf,black,self.rect.midleft,self.rect.midright,1)
        # origin
        pygame.draw.circle(self.surf,black,self.rect.center,self.rect.width/6,1)
        self.surf = self.surf.convert_alpha()
        self.orisurf = self.surf.copy()
        self.setCenter()
    def setCenter(self):
        self.rect.center = screenrect.center
        # we need x,y to move self.rect.center because self.rect.center is ALWAYS INT type.
        self.x,self.y = self.rect.center
    def speedUp(self):
        self.speed *= 1.05
    def speedDown(self):
        self.speed *= 0.90 
    def setSpeed(self,key):
        if key == pygame.K_k:
            self.speedUp()
        elif key == pygame.K_SPACE:
            self.speedDown()
    def startCar(self):
        self.start = True
        self.setDirection()
    def setDirection(self):
        self.dirx = -sin(self.angle*GRAD) 
        self.diry = -cos(self.angle*GRAD)

    def turn(self,key):
        ''' moving original surface, otherwise surface grows bigger and bigger
            eventually diverse '''
        if key == pygame.K_h: # turn left, counter-clockwise
            self.angle += +5.0 #self.rotatespeed
        elif key == pygame.K_l: # turn right, clockwise
            self.angle += -5.0 #self.rotatespeed
        else:
            return
        if self.angle > 360:
            self.angle += -360
        elif self.angle < -360:
            self.angle += 360
        self.surf = pygame.transform.rotate(self.orisurf, self.angle)
        self.rect = self.surf.get_rect(center= self.rect.center)
        self.setDirection()

    def move(self): # set speed
        if not self.start: return
        self.dx = self.dirx * self.speed
        self.dy = self.diry * self.speed
        # move surface by moving surface's center
        self.x += self.dx
        self.y += self.dy
        self.rect.center = int(self.x),int(self.y)

    def draw(self):
        bgsurf.blit( write(str(self.rect)) ,(20,40) )
        bgsurf.blit( write('center = ' + str(self.rect.center)), (20,60) )
        bgsurf.blit( write('angle = '  + str(self.angle)),    (20,80) )
        bgsurf.blit( write('speed = %.2f' %self.speed, purple),    (20,100) )
        bgsurf.blit(self.surf, self.rect)

darkness = 0.95
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
            elif e.key == pygame.K_s:
                car.startCar()
    #print t.rect.center
    bgsurf.fill(bgcolor)
    drawTracks()
    car.move()
    car.draw()
    screen.blit(bgsurf, (0,0))     # blit background on screen (overwriting all)
    pygame.display.flip()
    clock.tick(fps)


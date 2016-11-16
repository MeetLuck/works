"""
014-sprites.py
"""
import pygame,os, random
from colors import *
from vector import Vector

birdspeed = 20

def write(msg = 'Pygame'):
    font = pygame.font.SysFont('None',32)
    text = font.render(msg,True,black)
    text = text.convert_alpha()
    return text

class BirdCatcher(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.radius = 50
        w,h = self.radius*2,self.radius*2
        self.image = pygame.Surface((w,h))
        self.image.set_colorkey(black)
        pygame.draw.circle(self.image,red,(w/2,h/2),self.radius,2)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
    def update(self,seconds):
        self.rect.center = pygame.mouse.get_pos()

class Bird(pygame.sprite.Sprite):
    image = list()
    birds = dict()
    number = 0

    def __init__( self,startpos=(50,50) ):
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.Vp = Vector(startpos)
        self.image = Bird.image[0]
        self.rect = self.image.get_rect()
        self.newSpeed()
        self.catched = False

    def newSpeed(self):
        randomspeed = random.choice([-1,1])
        self.delta = Vector()
        self.delta.x = randomspeed + randomspeed*birdspeed*random.random()
        self.delta.y = randomspeed + randomspeed*birdspeed*random.random()

    def move(self,seconds):
        self.Vp += self.delta * seconds
        self.rect.center = tuple(self.Vp)

    def update(self,seconds):
        if self.catched:
            self.image = Bird.image[2]
        else:
            self.image = Bird.image[0]
        self.move(seconds)


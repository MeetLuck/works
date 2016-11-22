import pygame,os,sys
from random import randint,choice
from math import sin,cos,radians

class Creep(pygame.sprite.Sprite):
    def __init__(self,screen,game,creep_images,explosion_images,field,init_position,init_direction,speed):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.game = game
        self.speed = speed
        self.field = field
        self.baseimage0 = creep_images[0]
        self.baseimage45 = creep_images[1]
        self.image = self.baseimage0
        self.explosion_images = explosion_images
        self.direction = vec2d(init_direction).normalized()
        self.state = Creep.ALIVE
        self.health = 15
    def isAlive(self):
        return self.state in (Creep.ALIVE, Creep.EXPLODING)

# Game parameters
screensize = screenwidth,screenheight = 400,400
bgcolor = 150,150,80
creep_filenames = ['bluecreep.png','pinkcreep.png','grapycreep.png']
ncreeps = 20

pygame.init()
screen = pygame.display.set_mode(screensize,0,32)
clock = pygame.time.Clock()

# creates N Creeps random creeps
creeps = []
for i in range(ncreeps):
    c = Creep(screen, choice(CREEP_FILENAMES), 
            ( randint(0, screenwidth), randint(0, screenheight)), (choice([-1, 1]), choice([-1, 1])), 0.1))
    creeps.append(c)

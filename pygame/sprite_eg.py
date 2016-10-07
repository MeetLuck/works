import pygame, math, sys
from pygame.locals import *
screen = pygame.display.set_mode((1024,768))
fpsclock = pygame.time.Clock()
class CarSprite(pygame.sprite.Sprite):
    max_forward_speed = 10
    max_backward_speed = 10
    acceleration = 2
    turn_speed = 5

    def __init__(self,image,position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position
        self.speed = self.direction = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0
    def update(self,deltat):
        # simulation
        self.speed += self.k_up + self.k_down
        if self.speed > self.max_forward_speed:
            self.speed = self.max_forward_speed
        if self.speed < -self.backward_speed:
            self.speed = -self.backward_speed
        self.direction += self.k_right + self.k_left
        x,y = self.position
        rad = self.direction * math.pi/180
        x += -self.speed * math.sin(rad)
        y += -self.speed * math.cos(rad)
        self.position = x,y
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
# creae a car and run




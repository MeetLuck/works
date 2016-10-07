# Rapid Game Development with Python -> http://richard.cgpublisher.com/product/pub.84/prod.11
# Jones - RapidGameDev.pdf

import pygame, math, sys
from pygame.locals import *
screen = pygame.display.set_mode((1024,768))
fpsclock = pygame.time.Clock()
class PadSprite(pygame.sprite.Sprite):
    normal = pygame.image.load('pad_normal.png')
    hit = pygame.image.load('pad_hit.png')
    def __init__(self,number,position):
        pygame.sprite.Sprite.__init(self)
        self.number = number
        self.rect.center = position
        self.image = self.normal
pads = [
        PadSprite(1,(200,200)),
        PadSprite(2,(800,200)),
        PadSprite(3,(200,600)),
        PadSprite(4,(800,600)),
        ]


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
        if self.speed < -self.max_backward_speed:
            self.speed = -self.max_backward_speed
        self.direction += self.k_right + self.k_left
        x,y = self.position
        print 'old pos ->', self.position
        rad = self.direction * math.pi/180
        x += -self.speed * math.sin(rad)
        y += -self.speed * math.cos(rad)
        self.position = x,y
        print 'dir ->',self.direction
        print 'rad ->', rad
        print 'new pos ->',self.position
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
# creae a car and run
rect = screen.get_rect()
car = CarSprite('car.png',rect.center)
car_group = pygame.sprite.RenderPlain(car)
pad_group = pygame.sprite.RenderPlain(*pads)
collisions = pygame.sprite.spritecollide(car_group,pad_group)
current_pad_number = 0
while True:
    # user input
    deltat = fpsclock.tick(30)
    for e in pygame.event.get():
        if not hasattr(e,'key'): continue
        keydown = e.type == KEYDOWN
        if e.key == K_RIGHT: car.k_right = keydown * -1
        elif e.key == K_LEFT: car.k_left = keydown * +1
        elif e.key == K_UP: car.k_up = keydown * +2
        elif e.key == K_DOWN: car.k_down = keydown * -2 
        elif e.key == K_ESCAPE: sys.exit(0)
    pads = pygame.sprite.spritecollide(car,pad_group,False)
    if pads:
        pad = pads[0]
        if pad.number == current_pad_number +1:
            pad.image = pad.hit
            current_pad_number += 1
    elif current_pad_number == 4:
        for pad in pad_group.sprites(): pad.image = pad.normal
        current_pad_number = 0
    # rendering
    screen.fill((0,0,0))
    car_group.update(deltat)
    car_group.draw(screen)
    pad_group.update(collisions)
    pad_group.draw(screen)
    pygame.display.flip()




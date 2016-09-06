# import pygame modules
import pygame,time,math,sys
from pygame.locals import *
# basic screen initialisation
screen = pygame.display.set_mode((800,600))
class CarSprite(pygame.sprite.Sprite):
    max_forward_speed = 10
    max_reverse_speed = 10 
    acceleration = 2
    turn_speed = 5
    def __init__(self, image, position):
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
        if self.speed < -self.max_reverse_speed:
            self.speed = -self.max_reverse_speed
        self.direction += self.k_right + self.k_left
        x,y = self.position
        rad = self.direction * math.pi /180
        x += -self.speed * math.sin(rad)
        y += -self.speed * math.cos(rad)
        self.position = x,y
        self.image = pygame.transform.rotate(self.src_image,self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
# create a car and run
rect = screen.get_rect()
car = CarSprite('car2.bmp', rect.center)
car_group = pygame.sprite.RenderPlain(car)
while True:
    # user input
    deltat = pygame.time.Clock().tick(10)
    for event in pygame.event.get():
        if not hasattr(event,'key'): continue
        down = event.type == KEYDOWN
        if   event.key==K_RIGHT : car.k_right = -5 * down
        elif event.key==K_LEFT  : car.k_left  = +5 * down
        elif event.key==K_UP    : car.k_up    = +2 * down
        elif event.key==K_DOWN  : car.k_down  = -2 * down
        elif event.key==K_ESCAPE: sys.exit(0)

    # rendering
    screen.fill((255,255,255))
    car_group.update(deltat)
    car_group.draw(screen)
    pygame.display.flip()

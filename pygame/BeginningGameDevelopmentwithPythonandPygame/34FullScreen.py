# Listing 3-4. Full screen example
import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screensize = screenwidth,screenheight = 800,600
screen = pygame.display.set_mode(screensize,0,32)
bgsurf = pygame.image.load('sushiplate.jpg').convert()

# constants
Fullscreen = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT: pygame.quit(); exit()
        if event.type == KEYDOWN and event.key == K_f:
            Fullscreen = not Fullscreen
            if Fullscreen:
                screen = pygame.display.set_mode((640,480),FULLSCREEN,32)
            else:
                screen = pygame.display.set_mode((640,480),0,32)
    screen.blit(bgsurf,(0,0))
    pygame.display.update()


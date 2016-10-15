# Listing 5-1. Simple Straight-Line Movement
import pygame
from pygame.locals import *
from sys import exit

# constants
screensize = screenwidth,screenheight = 640,480
bgimage = 'sushiplate.jpg'
spriteimage = 'fugu.png'
black = pygame.Color('black')
green = pygame.Color('green')
blue = pygame.Color('blue')
white = pygame.Color('white')
 
# initialize pygame 
pygame.init()
screen = pygame.display.set_mode(screensize,0,32)
bgsurf = pygame.image.load(bgimage).convert()
spritesurf = pygame.image.load(spriteimage).convert_alpha()

x = 0
while True:
    for event in pygame.event.get():
        if event.type == QUIT: pygame.quit(); exit()
    screen.blit(bgsurf,(0,0))
    screen.blit(spritesurf, (x,100) )
    x += 1.0 
    # if image goes off the end of the screen, move it back
    if x > screen.get_width():
        x -= screenwidth
    pygame.display.update()


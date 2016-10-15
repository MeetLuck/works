# Listing 3-5. Using a Resizable Window
import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screensize = screenwidth,screenheight = 800,600
screen = pygame.display.set_mode(screensize,0,32)
bgsurf = pygame.image.load('sushiplate.jpg').convert()

# constants

while True:
    for event in pygame.event.get():
        if event.type == QUIT: pygame.quit(); exit()
        if event.type == VIDEORESIZE:
            screensize = event.size
            screen = pygame.display.set_mode(screensize,RESIZABLE,32)
            pygame.display.set_caption('Window resized to %s' %str(event.size) )
    # resize
    screewidth,screenheight = screensize
    for y in range(0,screenheight, bgsurf.get_height()):
        for x in range(0,screenwidth,bgsurf.get_width()):
            screen.blit(bgsurf,(x,y))
    pygame.display.update()


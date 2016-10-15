# Listing 3-3. Handling Keyboard Events
# font height = font.get_linesize()
import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screensize = screenwidth,screenheight = 800,600
screen = pygame.display.set_mode(screensize,0,32)
bgsurf = pygame.image.load('sushiplate.jpg').convert()
clock = pygame.time.Clock()
fps = 60

# constants
x,y = 0,0
deltaX,deltaY = 0,0
black = pygame.Color('black')

while True:
    for event in pygame.event.get():
        if event.type == QUIT: pygame.quit(); exit()
        if event.type == KEYDOWN:
            if   event.key == K_LEFT:  deltaX = -1
            elif event.key == K_RIGHT: deltaX = +1
            elif event.key == K_UP:    deltaY = -1
            elif event.key == K_DOWN:  deltaY = +1
        elif event.type == KEYUP:
            # stop movement by RESETting deltaX,deltaY 
            if   event.key == K_LEFT:  deltaX = 0
            elif event.key == K_RIGHT: deltaX = 0
            elif event.key == K_UP:    deltaY = 0
            elif event.key == K_DOWN:  deltaY = 0

    # move as long as key's down  because deltaX, deltaY is NOT zero
    x += deltaX
    y += deltaY

    screen.fill(black)
    screen.blit(bgsurf, (x,y))
    pygame.display.update()
    #clock.tick(fps)



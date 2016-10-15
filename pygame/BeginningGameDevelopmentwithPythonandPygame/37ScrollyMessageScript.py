# Listing 3-7. Scrolly Message Script
import pygame
from pygame.locals import *
from sys import exit

# constants
screensize = screenwidth,screenheight = 600,480
msg = '   This is a demonstration of the scrolly message script.   '
blue = pygame.Color('blue')
white = pygame.Color('white')
 
# initialize pygame 
pygame.init()
screen = pygame.display.set_mode(screensize,0,32)
bgsurf = pygame.image.load('sushiplate.jpg').convert()

# font object
font = pygame.font.SysFont('bitstreamveraserif',80)
textsurf = font.render(msg,True,blue) # font.render(text,antialias,fg,bg)
x = 0
y = (screenheight - textsurf.get_height() )/2.0

while True:
    for event in pygame.event.get():
        if event.type == QUIT: pygame.quit(); exit()

    x -= 1
    if x < -textsurf.get_width():
        x = 0
    screen.blit(bgsurf,(0,0))
    screen.blit( textsurf,(x,y) )
    screen.blit( textsurf, (x+textsurf.get_width(), y) )
    pygame.display.update()

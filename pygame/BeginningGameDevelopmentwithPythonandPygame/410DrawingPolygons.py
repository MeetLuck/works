# Listing 4-10. Drawing Polygons with Pygame
import pygame
from pygame.locals import *
from sys import exit

# constants
screensize = screenwidth,screenheight = 640,480
msg = '   This is a demonstration of the scrolly message script.   '
black = pygame.Color('black')
green = pygame.Color('green')
blue = pygame.Color('blue')
white = pygame.Color('white')
 
# initialize pygame 
pygame.init()
screen = pygame.display.set_mode(screensize,0,32)

points = list()

while True:
    for event in pygame.event.get():
        if event.type == QUIT: pygame.quit(); exit()
        if event.type == MOUSEBUTTONDOWN:
            points.append(event.pos)
    screen.fill(white)
    if len(points) >= 3:
        pygame.draw.polygon(screen, green, points)
    for point in points:
        pygame.draw.circle(screen,blue,point,5)
    pygame.display.update()


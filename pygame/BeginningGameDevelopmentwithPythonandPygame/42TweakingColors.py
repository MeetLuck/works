# Listing 4-2. Script for Tweaking Colors
import pygame
from pygame.locals import *
from sys import exit

# constants
screensize = screenwidth,screenheight = 640,480
msg = '   This is a demonstration of the scrolly message script.   '
black = pygame.Color('black')
blue = pygame.Color('blue')
white = pygame.Color('white')
 
# initialize pygame 
pygame.init()
screen = pygame.display.set_mode(screensize,0,32)

# creates images with smooth gradients
def createScales(height):
    redsurf = pygame.surface.Surface( (640,height))
    greensurf = pygame.surface.Surface( (640,height))
    bluesurf = pygame.surface.Surface( (640,height))
    for x in range(640): # 0,1,2 ... 639
        c = int( 255 * x/639.0 )
        red   = c,0,0
        green = 0,c,0
        blue  = 0,0,c
        linerect = Rect(x,0,1,height)
        pygame.draw.rect(redsurf, red, linerect)
        pygame.draw.rect(greensurf, green, linerect)
        pygame.draw.rect(bluesurf, blue, linerect)
    return redsurf,greensurf,bluesurf

redsurf,greensurf,bluesurf = createScales(80)

color = [127,127,127]

while True:
    for event in pygame.event.get():
        if event.type == QUIT: pygame.quit(); exit()

    screen.fill(black)
    # draw the scales to the screen
    screen.blit(redsurf,(0,00))
    screen.blit(greensurf,(0,80))
    screen.blit(bluesurf,(0,160))

    x,y = pygame.mouse.get_pos()

    # if mouse was pressed on one of the sliders, adjust the color component
    if pygame.mouse.get_pressed()[0]: # left button
        for component in (0,1,2):
            if 80*component < y < 80*(component+1):
                color[component] =  int( 255 * x/639.0 )  # screen.get_width() = 639
                print x, color
        pygame.display.set_caption('Pygame Color Test - %s' %str(color) )

    # draw a circle for each slider to represent the current setting
    for component in (0,1,2):
        pos = int( 639*color[component]/255 ), 80*component + 40
        pygame.draw.circle(screen, white, pos,10)

    pygame.draw.rect(screen, color, (0,240,640,240) )
    pygame.display.update()


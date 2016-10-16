# Listing 8-1 Illusion of Depth

import pygame
from pygame.locals import *

from random import randint, choice
from gameobjects.vector2 import Vector2

# constants
screensize = screenwidth,screenheight = 640,480
fps = 60
black = pygame.Color('black')
white = pygame.Color('white')

class Star(object):
    def __init__(self,x,y,speed):
        self.x, self.y = x,y
        self.speed = speed

def run():
    pygame.init()
    screen = pygame.display.set_mode( screensize, FULLSCREEN)
    stars = []

    # Add a few stars for the first time
    for i in xrange(200):
        x = randint(0,screenwidth-1)
        y = randint(0,screenheight-1)
        speed = randint(10,300)
        stars.append( Star(x,y,speed) )

    clock = pygame.time.Clock()

    while True:
        for e in pygame.event.get():
            if e.type==QUIT or e.type==KEYDOWN:
                return
        # add a new star
        y = randint(0,screenheight-1)
        speed = randint(10,300)
        star = Star( screenwidth, y, speed )
        stars.append(star)
        timepassed = clock.tick(fps)/1000.0
        screen.fill(black)
        # draw stars
        for star in stars:
            x = star.x - timepassed * star.speed
            pygame.draw.aaline(screen,white,(x,star.y),(star.x+1,star.y) )
            star.x = x
        def onScreen(star):
            return star.x > 0
        # remove stars that are no longer visible
        stars = filter(onScreen, stars)
        pygame.display.update()

if __name__ == '__main__':
    run()


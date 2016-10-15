import pygame, sys
from pygame.locals import *

# initialize all imported pygame modules
pygame.init()
# pygame.display.set_mode(resolution=(0,0),flags=0, depth=0)
# initialize window
surface = pygame.display.set_mode((400,300))
# set title
pygame.display.set_caption('Hello World')
# run game loop
while True:
    for event in pygame.event.get(): # get events from queue
        if event.type == quit:
            pygame.quit(); sys.exit()
    pygame.display.update()

"transparent Colors"
# to draw using transparent colors, create a Surface object with convert_alpha()method
# anotherSurface = surface.convert_alpha()

"pygame.Color object"
# pygame.Color(r,g,b,alpha)
# pygame.Color(name)  e.g. pygame.Color('black')
# pygame.color.THECOLORS

"rect objects"
# x,y,w,h
# left,top,width,height
# rect = pygame.Rect(x,y,w,h)
# rect = pygame.Rect(left,top,width,height)
# rect = pygame.Rect((left,top),(width,height))
# right  = left + width = x + w
# bottom = top + height = y + h
# rect.size : (w,h)
# rect.topleft : (x,y)
# rect.bottomright : (right,bottom)

import pygame, sys
from pygame.locals import *

# init pygame module
pygame.init()

# set up the window
surface = pygame.display.set_mode((500,400),0,32)
pygame.display.set_caption('Drawing Example')

# set up the colors
black = pygame.Color('black')
white = pygame.Color('white')
red = pygame.Color('red')
green = pygame.Color('green')
blue = pygame.Color('blue')

# draw on the surface
surface.fill(white)
# pygame.draw.polygon(surface,color,pointlist,width)
# pygame.draw.line(surface,color,start,end,width)
# pygame.draw.lines(surface,color,closed,pointlist,width)
# pygame.draw.circle(surface,color,center,radius,width)
# pygame.draw.ellipse(surface,color,bounding_rectangle,width)
# pygame.draw.rect(surface,color,bounding_rectangle,width)
pygame.draw.polygon(surface, green, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
pygame.draw.line(surface, blue, (60, 60), (120, 60), 4)
pygame.draw.line(surface, blue, (120, 60), (60, 120))
pygame.draw.line(surface, blue, (60, 120), (120, 120), 4)
pygame.draw.circle(surface, blue, (300, 50), 20, 0)
pygame.draw.ellipse(surface, red, (300, 250, 40, 80), 1)
pygame.draw.rect(surface, red, (200, 150, 100, 50))

# draw pixel
pixobj = pygame.PixelArray(surface)
import time
time.sleep(0.5)
for down in range(20):
    pixobj[200,80+down] = black
    pygame.display.flip()
    time.sleep(0.1)
del pixobj

# run the game loop
while True:
    for e in pygame.event.get():
        if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE:
            pygame.quit(); sys.exit()
            sys.exit()
    pygame.display.update()

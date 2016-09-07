import pygame,sys
from pygame.locals import *

pygame.init()

FPS = 30 # Frames Per Second
fpsclock = pygame.time.Clock()

# set up the window
surface = pygame.display.set_mode( (400,300),0,32)
pygame.display.set_caption('Cat Animation')

white = 255,255,255
catimg = pygame.image.load('cat.png')
catx,caty = 10,10
direction = 'right'

while True:
    surface.fill(white)
    if direction == 'right':
        catx += 5
        if catx == 280: direction = 'down'
    elif direction == 'down':
        caty += 5
        if caty == 220: direction = 'left'
    elif direction == 'left':
        catx += -5
        if catx == 10: direction = 'up'
    elif direction == 'up':
        caty += -5
        if caty == 10: direction = 'right'
    surface.blit(catimg,(catx,caty))
    for e in pygame.event.get():
        if e.type == QUIT or e.type==KEYDOWN and e.key==K_ESCAPE:
            pygame.quit(); sys.exit()
    pygame.display.update()
    fpsclock.tick(FPS)

" Drawing images with pygame.image.load() and blit() "
# pygame.image.load() will return a Surface object that has the image drawn on it.
# this surface object will be a seperate Surface object from the display Surface object,
# so we must blit(copy) the image's Surafce object to the display Surface object.
# blitting is drawing the contents of one Surface onto another.

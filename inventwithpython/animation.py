import pygame, sys, time
from pygame.locals import *
# set up pygame
pygame.init()
# set up the window
windowwidth, windowheight = 400,400
windowSurface = pygame.display.set_mode((windowwidth,windowheight),0,32)
pygame.display.set_caption('Animation')
# set up directions variables
downleft,downright,upleft,upright = 1,3,7,9
movespeed = 4
# set up the colors
black = 0,0,0
white = 255,255,255
red   = 255,0,0
green = 0,255,0
blue  = 0,0,255
# set up the block data structure
b1={'rect':pygame.Rect(300,80,50,100),'color':red, 'dir':upright}
b2={'rect':pygame.Rect(200,200,20,20),'color':green, 'dir':upleft}
b3={'rect':pygame.Rect(100,150,60,60),'color':blue, 'dir':downleft}
blocks = [b1,b2,b3]

# run the game loop
while True:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # draw the black background onto the surface
    windowSurface.fill(black)
    for b in blocks:
        # move the block data structure
        if b['dir'] == downleft:
            b['rect'].left += -movespeed
            b['rect'].top  += +movespeed
        if b['dir'] == downright:
            b['rect'].left += +movespeed
            b['rect'].top  += +movespeed
        if b['dir'] == upleft:
            b['rect'].left += -movespeed
            b['rect'].top  += -movespeed
        if b['dir'] == upright:
            b['rect'].left += +movespeed
            b['rect'].top  += -movespeed
        # check if the block has move out of the window
        if b['rect'].top < 0:
            # block has moved past the top
            if b['dir'] == upleft : b['dir'] = downleft
            if b['dir'] == upright: b['dir'] = downright
        if b['rect'].bottom > windowheight:
            # block has moved past the bottom
            if b['dir'] == downleft : b['dir'] = upleft
            if b['dir'] == downright: b['dir'] = upright
        if b['rect'].left < 0 :
            # block has moved past the left side
            if b['dir'] == downleft : b['dir'] = downright
            if b['dir'] == upleft:    b['dir'] = upright
        if b['rect'].right > windowwidth:
            # block has moved past the right side
            if b['dir'] == downright: b['dir'] = downleft
            if b['dir'] == upright:   b['dir'] = upleft
        # draw the block onto the surface
        pygame.draw.rect(windowSurface,b['color'],b['rect'])
    # draw the window onto the screen
    pygame.display.update()
    time.sleep(0.02)

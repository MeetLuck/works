import pygame, sys, random
from pygame.locals import *

def doRectsOverlap(rect1,rect2):
    for a,b in [(rect1,rect2),(rect2,rect1)]:
        # check if a's corners are inside b
        if isPointInsideRect(a.left,a.top,b) or \
           isPointInsideRect(a.left,a.bottom,b) or \
           isPointInsideRect(a.right,a.top,b) or \
           isPointInsideRect(a.right, a.bottom,b):
               return True

    return False

def isPointInsideRect(x,y,rect):
    if (rect.left < x < rect.right) and (rect.top < y < rect.bottom):
        return True
    else:
        return False

# set up pygame
pygame.init()
mainclock = pygame.time.Clock()
# set up the window
windowwidth,windowheight = 400,400
windowSurface = pygame.display.set_mode((windowwidth, windowheight),0,32)
pygame.display.set_caption('Collision detection')
# set up direction variables
downleft,downright,upleft,upright = 1,3,7,9
movespeed = 4
# set up the colors
black = 0,0,0
green = 0,255,0
white = 255,255,255
# set up the bouncer and food data structures
foodcounter = 0
newfood = 40
foodsize = 20
bouncer = {'rect':pygame.Rect(300,100,50,50),'dir':upleft}
foods = []
for i in range(20):
    foods.append(pygame.Rect(random.randint(0,windowwidth-foodsize), random.randint(0,windowheight-foodsize), foodsize, foodsize))
# run the game loop
while True:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    foodcounter += 1
    if foodcounter >= newfood:
        # add new food
        foods.append(pygame.Rect(random.randint(0,windowwidth-foodsize), random.randint(0,windowheight-foodsize), foodsize, foodsize))
    # draw the black background
    windowSurface.fill(black)
    # move the bouner data structure
    if bouncer['dir'] == downleft:
        bouncer['rect'].left += -movespeed
        bouncer['rect'].top  += +movespeed
    if bouncer['dir'] == downright:
        bouncer['rect'].left += +movespeed
        bouncer['rect'].top  += +movespeed
    if bouncer['dir'] == upleft:
        bouncer['rect'].left += -movespeed
        bouncer['rect'].top  += -movespeed
    if bouncer['dir'] == upright:
        bouncer['rect'].left += +movespeed
        bouncer['rect'].top  += -movespeed
    # check if the bouncer has move out of the window
    if bouncer['rect'].top < 0:
        # bouncer has moved past the top
        if bouncer['dir'] == upleft:  bouncer['dir'] = downleft
        if bouncer['dir'] == upright: bouncer['dir'] = downright
    if bouncer['rect'].bottom > windowheight:
        # bouncer has moved past the bottom
        if bouncer['dir'] == downleft:  bouncer['dir'] = upleft
        if bouncer['dir'] == downright: bouncer['dir'] = upright
    if bouncer['rect'].left < 0:
        # bouncer has moved past the left side
        if bouncer['dir'] == downleft:  bouncer['dir'] = downright
        if bouncer['dir'] == upleft: bouncer['dir'] = upright
    if bouncer['rect'].right > windowwidth:
        # bouncer has moved past the right side
        if bouncer['dir'] == downright: bouncer['dir'] = downleft
        if bouncer['dir'] == upright:   bouncer['dir'] = upleft
    # draw the bouncer onto the surface
    pygame.draw.rect(windowSurface,white,bouncer['rect'])
    # check if the bouncer has intersected with any food squares
    for food in foods[:]:
        if doRectsOverlap(bouncer['rect'],food):
            foods.remove(food)
    # draw the food
    for i in range(len(foods)):
        pygame.draw.rect(windowSurface, green, foods[i])
    # draw the window
    pygame.display.update()
    mainclock.tick(40)





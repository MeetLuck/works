import pygame, sys, random
from pygame.locals import *
# setup pygame
pygame.init()
mainclock = pygame.time.Clock()
# setup the window
windowwidth, windowheight = 400,400
windowSurface = pygame.display.set_mode((windowwidth,windowheight),0,32)
pygame.display.set_caption('keyborad Input')
# setup the colors
black = 0,0,0
green = 0,255,0
white = 255,255,255
# setup the player and food datat structure
foodcounter = 0
newfood = 40
foodsize = 20
player = pygame.Rect(300,100,50,50)
foods = list()
for i in range(20):
    foods.append(pygame.Rect(random.randint(0,windowwidth-foodsize),random.randint(0,windowheight-foodsize),foodsize,foodsize))
# setup the movement variables
moveleft,moveright,moveup,movedown = False,False,False,False
movespeed = 6
# run the game loop
while True:
    # check for events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # change the keyboard variables
            if event.key == K_LEFT or event.key == ord('a'):
                moveright = False
                moveleft  = True
            if event.key == K_RIGHT or event.key == ord('d'):
                moveleft = False
                moveright  = True
            if event.key == K_UP or event.key == ord('w'):
                movedown = False
                moveup  = True
            if event.key == K_DOWN or event.key == ord('s'):
                moveup = False
                movedown  = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == ord('a'):
                moveleft = False
            if event.key == K_RIGHT or event.key == ord('d'):
                moveright = False
            if event.key == K_UP or event.key == ord('w'):
                moveup = False
            if event.key == K_DOWN or event.key == ord('s'):
                movedown = False
            if event.key == ord('x'):
                player.top = random.randint(0,windowheight-player.height)
                player.left = random.randint(0,windowwidth-player.width)
        if event.type == MOUSEBUTTONUP:
            foods.append(pygame.Rect(event.pos[0], event.pos[1],foodsize,foodsize))
    foodcounter += 1
    if foodcounter >= newfood:
        # add new food
        foodcounter = 0
        foods.append(pygame.Rect(random.randint(0,windowwidth-foodsize), random.randint(0,windowheight-foodsize),foodsize,foodsize))
    # draw the black background
    windowSurface.fill(black)
    # move the player
    if movedown and player.bottom < windowheight: player.top += movespeed
    if moveup and player.top > 0: player.top += -movespeed
    if moveleft and player.left > 0: player.left += -movespeed
    if moveright and player.right < windowwidth: player.right += movespeed
    # draw the player
    pygame.draw.rect(windowSurface,white,player)
    # check if the player has intersected with any food
    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food)
    # draw the food
    for i in range(len(foods)):
        pygame.draw.rect(windowSurface,green,foods[i])
    # draw the window
    pygame.display.update()
    mainclock.tick(40)




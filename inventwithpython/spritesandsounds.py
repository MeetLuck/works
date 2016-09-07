# a sprite is a name for a single two-dimensional image that is used as partof the graphics
import pygame,sys,random
from pygame.locals import *

# setup pygame
pygame.init()
mainclock = pygame.time.Clock()
# set up the window
windowwidth,windowheight = 400,400
windowsurface = pygame.display.set_mode((windowwidth,windowheight),0,32)
pygame.display.set_caption('Sprites and Sound')
# set up the colors
black = 0,0,0

# set up the block data
player = pygame.Rect(300,100,40,40)
playerimage = pygame.image.load('player.png')
playerstretchedimage = pygame.transform.scale(playerimage,(40,40))
foodimage = pygame.image.load('cherry.png')
foods = list()
for i in range(20):
    foods.append(pygame.Rect(random.randint(0,windowwidth-20), random.randint(0,windowheight-20),20,20))
foodcounter = 0
newfood = 40

# set up the keyboard variables
moveleft,moveright,moveup,movedown = False,False,False,False
movespeed = 6

# set up music
pickupsound = pygame.mixer.Sound('pickup.wav')
pygame.mixer.music.load('background.mid')
pygame.mixer.music.play(-1,0.0)
musicplaying = True


# run the game loop
while True:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            # change the keyboard variable
            if event.key == K_LEFT or event.key == ord('a'):
                moveright = False
                moveleft = True
            if event.key == K_RIGHT or event.key == ord('s'):
                moveleft = False
                moveright = True
            if event.key == K_UP or event.key == ord('d'):
                movedown = False
                moveup = True
            if event.key == K_DOWN or event.key == ord('f'):
                moveup = False
                movedown = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == ord('a'):
                moveleft = False
            if event.key == K_RIGHT or event.key == ord('s'):
                moveright = False
            if event.key == K_UP or event.key == ord('d'):
                moveup = False
            if event.key == K_DOWN or event.key == ord('f'):
                movedown = False
            if event.key == ord('x'):
                # teleport player
                player.top = random.randint(0,windowheight-player.height)
                player.left = random.randint(0,windowwidth-player.width)
            if event.key == ord('m'):
                if musicplaying:
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.play(-1,0.0)
                musicplaying = not musicplaying

        if event.type == MOUSEBUTTONUP:
            foods.append(pygame.Rect(event.pos[0]-10,event.pos[1]-10,20,20))

    foodcounter += 1
    if foodcounter >= newfood:
        # add new food
        foodcounter = 0
        foods.append(pygame.Rect(random.randint(0,windowwidth-20),random.randint(0,windowheight-20),20,20))
    # draw the black background
    windowsurface.fill(black)
    # move the player
    if movedown and player.bottom < windowheight:
        player.top += movespeed
    if moveup and player.top > 0:
        player.top += -movespeed
    if moveleft and player.left > 0:
        player.left += -movespeed
    if moveright and player.right < windowwidth:
        player.right += movespeed
    # draw the block
    windowsurface.blit(playerstretchedimage,player)
    # check if the block has intersected with any food squares
    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food)
            player = pygame.Rect(player.left,player.top,player.width+2, player.height+2)
            playerstrectedimage = pygame.transform.scale(playerimage, (player.width,player.height))
            if musicplaying:
                pickupsound.play()
    # draw the food
    for food in foods:
        windowsurface.blit(foodimage, food)
    # draw the window
    pygame.display.update()
    mainclock.tick(40)




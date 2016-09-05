import pygame, sys, time, random
from pygame.locals import *
# setup pygame
pygame.init()
mainClock = pygame.time.Clock()
# setup the window
windowwidth, widowheight = 400,400
windowsurface = pygame.display.set_mode( (windowwidth, windowheight),0,32)
pygame.display.set_caption('Sprites and Sound')
# setup the colors
black = (0,0,0)
# setup the block data structure
player = pygame.Rect(300,100,40,40)
playerImage = pygame.image.load('player.png')
playerStretchedImage = pygame.transform.scale(playerImage,(40,40))
foodImage = pygame.image.load('cherry.png')
foods = []
for i in range(20):
    foods.append(pygame.Rect(random.randint(0,windowwidth-20), random.randint(0,widowheight-20),20,20))
foodCounter = 0
newfood = 40
# setup keyboard variables
moveLeft,moveRight,moveUp,moveDown = False,False,False,False
movespeed = 6
# setup music
pickUpSound = pygame.mixer.Sound('pickup.wav')
pygame.mixer.music.load('background.mid')
pygame.mixer.music.play(-1,0.0)
musicPlaying = True

# run the game loop
while True:
    # check for the quit event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # change the keyboard variables
            if event.key = K_LEFT or event.key == ord('a'):
                moveRight = False
                moveLeft = True
            if event.key = K_RIGHT or event.key == ord('d'):
                moveLeft = False
                moveRight = True
            if event.key = K_UP or event.key == ord('w'):
                moveDown = False
                moveUp = True
            if event.key = K_DOWN event.key == ord('a'):
                moveUp = False
                moveDown = True
        if event.type == KEYUP:
            if event.key = K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key = ord('a'):
                moveLeft = False
            if event.key == K_RIGHT or event.key = ord('d'):
                moveRight = False
            if event.key == K_UP or event.key = ord('w'):
                moveUp = False
            if event.key == K_DOWN or event.key = ord('s'):
                moveDown = False
            if event.key == ord('x'):
                player.top = random.randint(0, windowheight - player.height)
                player.left = random.randint(0, windowwidth - player.width)
            if event.key == ord('m'):
                if musicPlaying:
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.play(-1,0.0)
                musicPlaying = not musicPlaying
        if event.type == MOUSEBUTTONUP:




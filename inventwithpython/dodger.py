import pygame, random, sys
from pygame.locals import *

width,height = 600,600
windowsize = width,height
textcolor = 255,255,255
backgroundcolor=0,0,0
fps = 40
badditeminsize,badditemaxsize = 10,40
badditeminspeed, badditemaxspeed = 1,8
addnewbaddierate = 6
playermoverate = 5

def terminate():
    pygame.quit()
    sys.exit()

def waitforplayertopresskey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

def playerhashitbaddie(playerRect,baddies):
    for b in baddies:
        if playerRect.colliderect( b['rect'] ):
            return True
    return False

def drawtext(text,font,surface,x,y):
    textobj = font.render(text,1,textcolor)
    textrect = textobj.get_rect()
    textrect.topleft = x,y
    surface.blit(textobj,textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainclock = pygame.time.Clock()
windowsurface = pygame.display.set_mode(windowsize)
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)
# set up fonts
font = pygame.font.SysFont(None,48)
# set up sounds
gameoversound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')
# set up images
playimage = pygame.image.load('player.png')
playerRect = playerimage.get_rect()
baddieimage = pygame.image.load('baddie.png')
# show the start screen
drawtext('Dodger',font, windowsurface,width/3,height/3)
drawtext('Press a key to start.', font, windowsurface, width/3 - 30, height/3 + 50)
pygame.display.update()
waitforplayertopresskey()

topscore = 0
while True:
    # setup the start of the game
    baddies = list()
    score = 0
    playerRect.topleft = width/2, height-50
    moveleft = moveright = moveup = movedown = False
    reversecheat = showcheat = False
    baddieaddcounter = 0
    pygame.mixer.music.play(-1,0.0)

    while True: # the game loop runs while the game part is playing
        score += 1 # increase score
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reversecheat = True
                if event.key == ord('x'):
                    slowcheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveright, moveleft = False,True
                if event.key == K_RIGHT or event.key == ord('s'):
                    moveleft, moveright = False,True
                if event.key == K_UP or event.key == ord('d'):
                    movedown, moveup = False,True
                if event.key == K_DOWN or event.key == ord('f'):
                    moveup, movedown = False,True
            if event.type == KEYUP:
                if event.key == ord('z'):
                    reversecheat = False
                    score = 0
                if event.key == ord('x'):
                    slowcheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_LEFT or event.key == ord('a'):
                    moveleft = False
                if event.key == K_RIGHT or event.key == ord('s'):
                    moveright = False
                if event.key == K_UP or event.key == ord('d'):
                    moveup = False
                if event.key == K_DOWN or event.key == ord('f'):
                    movedown = False
            if event.type == MOUSEMOTION:
                # if the mouse moves, move the player where the cursor is
                playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)
        # add new baddies at the top of the screen if needed
        if not reversecheat and not slowcheat:
            baddieaddcounter += 1
        if baddieaddcounter == addnewbaddierate:
            baddieaddcounter = 0
            baddiesize = random.ranint(baddieminsize,baddiemaxsize)
            newbaddie = {'rect':pygame.Rect(random.randint(0,width-baddiesize),0-baddiesize, baddiesize,baddiesize),
                    'speed':random.randint(baddieminspeed,baddemaxspeed),
                    'surface':pygame.transform.scale(baddieimage,(baddiesize,baddiesize)),
                    }
            baddies.append(newbaddie)
        # move the player around
        if moveleft and playerRect.left > 0:
            playerRect.move_ip(-1 * playermoverate,0)
        if moveright and playerRect.right < width:
            playerRect.move_ip(playermoverate,0)
        if moveup and playerRect.top > 0:
            playerRect.move_ip(0,-1*playermoverate)
        if movedown and playerRect.bottom < height:
            playerRect.move_ip(0, playermoverate)
        # move the baddies down
        for b in baddies:
            if not reversecheat and not slowcheat:
                b['rect'].move_ip(0, b['speed'])
            elif reversecheat:
                b['rect'].move_ip(0,-5)
            elif slowcheat:
                b['rect'].move_ip(0,1)
        # delete baddies that have fallen past the bottom
        for b in baddies[:]:
            if b['rect'].top > height:
                baddies.remove(b)
        # draw the game world on the window
        windowsurface.fill(backgroundcolor)
        # draw the score and top score
        drawtext('Score: %s' % score, font, windowsurface,10,0)
        drawtext('Top Score: %s' % topscore, font, windowsurface,10,40)
        # draw the player's rectangle
        windowsurface.blit(playerimage, playerRect)
        # draw each baddie
        for b in baddies:
            windowsurface.blit( b['surface'], b['rect'])
        pygame.display.update()
        # check if any of the baddies have hit the player
        if playerhashitbaddie(playerRect, baddies):
            if score > topscore:
                topscore = socre
            break
        mainclock.tick(fps)
    # stop the game and show the game over screen
    pygame.mixer.music.stop()
    gameoversound.play()
    drawtext('Game Over', font, windowsurface, width/3, height/3)
    drawtext('Press a key to play again', font, windowsurface, width/3-80, height/3+50)
    pygame.display.update()
    waitforplayertopresskey()
    gameoversound.stop()

    





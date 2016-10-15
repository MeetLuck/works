from Component2 import *

def main():
    global fpsclock, screen,displaysurf,displayrect, basicfont, l_squir_img, r_squir_img, grassImages
    pygame.init()
    fpsclock = pygame.time.Clock()
    pygame.display.set_icon(pygame.image.load('gameicon.png'))
    screen = pygame.display.set_mode( (3*winwidth,3*winheight))
    displaysurf = pygame.Surface( (winwidth,winheight))
    displayrect = displaysurf.get_rect()
    displayrect.topleft = winwidth,winheight
    basicfont = pygame.font.Font('freesansbold.ttf',32)
    pygame.display.set_caption('Squirrel eat Squirrel')
    while True:
        runGame()

def runGame():
    # setup variables for the start of a new game
    gameOverMode = False # if the player has lost
    gameOverStartTime = 0 # time the player lost
    winMode = False       # if the player has won
    # create the surfaces to hold game text
    gameOverSurf,gameOverRect = getTextObj(basicfont,'GameOver',white,winwidth/2,winheight/2)
    winSurf,winRect = getTextObj(basicfont,'You have achieved OMEGA SQUIRREL!',white,winwidth/2,winheight/2)
    winSurf2,winRect2 = getTextObj(basicfont,'Press "r" to restart',white,winwidth/2,winheight/2+30)

    # camerax and cameray are where the middle of the camera view is
    camerax,cameray = 0,0

    # store grass, squirrel, player
    grasses = [] 
    squirrels = []
    player = Player()
    direction = Direction()
    # start off with some random grass images on the screen
    for i in range(10):
        grasses.append( Grass(camerax,cameray) )
        grasses[i].x = random.randint(0,winwidth)
        grasses[i].y = random.randint(0,winheight)


    #print camerax

    while True: # main game loop
        # check if we should turn off invulnerability
        if player.invulnerable and time.time() - player.invulnerableStartTime > invulntime:
            player.invulnerable = False
        # move all the squirrels
        for squirrel in squirrels: # move the squirrel, and adjust for their bounce
            squirrel.move()

        # go through all the objects and see if any need to be deleted
        for i in range( len(grasses)-1,-1,-1):
            if isOutsideActiveArea(camerax,cameray,grasses[i]):
                del grasses[i]
        for i in range( len(squirrels)-1,-1,-1):
            if isOutsideActiveArea(camerax,cameray,squirrels[i]):
                del squirrels[i]

        # add more grass & squirrels if we dont' have enough
        while len(grasses) < numgrass:
            grasses.append(Grass(camerax,cameray))
        while len(squirrels) < numsquirrels:
            squirrels.append(otherSquirrel(camerax,cameray))

        #print camerax
        # adjust camerax and cameray if beyond the 'camera slack'
        if (camerax + winwidth/2) - player.centerX > cameraslack: # camera.centerX > player.centerX
            camerax = (player.centerX - winwidth/2) + cameraslack
        elif player.centerX - (camerax+winwidth/2) > cameraslack: # camera.centerX < player.centerX
            camerax = (player.centerX - winwidth/2) - cameraslack

        if (cameray + winheight/2) - player.centerY > cameraslack: # camera.centerY > player.centerY
            cameray = player.centerY - winheight/2 + cameraslack 
        elif player.centerY - (cameray+winheight/2) > cameraslack: # camera.centerY < player.centerY
            cameray = player.centerY - winheight/2 - cameraslack



        for event in pygame.event.get():
            if event.type == QUIT: terminate()
            elif event.type == KEYDOWN:
                if event.key in (K_UP,K_w):         direction.down,direction.up = False,True
                elif event.key in (K_DOWN, K_s):    direction.down,direction.up = True, False
                elif event.key in (K_LEFT,K_a):     direction.left,direction.right = True,False
                elif event.key in (K_RIGHT,K_d):    direction.left,direction.right = False,True
                elif winMode and event.key == K_r:
                    print 'You Win'
                    pygame.time.wait(2000)
                    return
            elif event.type == KEYUP:
                # stop moving the player's squirrel
                if event.key in (K_LEFT,K_a):       direction.left = False
                elif event.key in (K_RIGHT,K_d):    direction.right = False
                elif event.key in (K_UP,K_w):       direction.up = False
                elif event.key in (K_DOWN,K_s):     direction.down = False
                elif event.key == K_ESCAPE: terminate()
        if not gameOverMode:
            # actually move the player
            player.move(direction)
            # check if the player has collided with any squirrels
            for i in range( len(squirrels)-1, -1,-1):
                squirrel = squirrels[i]
                if player.isCollideWith(squirrel):    # a player/squirrel collsion has occured
                    if player.isLargerThan(squirrel): # player is larger and eats the squirrel
                        player.makeLarge(squirrel)
                        print 'size: ',player.width
                        if player.width > winsize:
                            winMode = True # turn on 'win mode'
                        del squirrels[i]
                    #elif not invulnerableMode: # player is smaller and takes damage
                    else:
                        player.setDamage()
                        if player.health == 0:
                            gameOverMode = True # turn on 'gameover mode'
                            gameOverStartTime = time.time()

        else: # game is over, show 'gameover' text
            displaysurf.blit(gameOverSurf,gameOverRect)
            if time.time() - gameOverStartTime > gameovertime:
                return # end the current game


        # draw the green background
        screen.fill(pygame.Color('gray'))
        #displaysurf.fill(grasscolor)
        #displaysurf.fill(pygame.Color('darkgray'))
        pointlist = [camerax,cameray],[camerax+winwidth,cameray],[camerax+winwidth,cameray+winheight],\
        [camerax,cameray+winheight]
        pygame.draw.lines(screen,red,True,pointlist)
        for grass in grasses:
            grass.draw(screen,camerax=0,cameray=0)
            #grass.draw(displaysurf,camerax=0,cameray=0)
        for squirrel in squirrels:
            squirrel.draw(screen,camerax=0,cameray=0)
            #squirrel.draw(displaysurf,camerax,cameray)
        # draw the player squirrel
        flashIsOn = round(time.time(),1) * 10 % 2 == 1
        if not gameOverMode and not (player.invulnerable and flashIsOn):
            player.draw(screen,camerax=0,cameray=0)
            #player.draw(displaysurf,camerax=0,cameray=0)
        # draw the health meter
        drawHealthMeter(player.health)

        # check if the player has won
        if winMode:
            displaysurf.blit(winSurf,winRect)
            displaysurf.blit(winSurf2,winRect2)
        #screen.blit(displaysurf,displayrect)
        pygame.display.update()
        fpsclock.tick(fps)

#------------ helpers -----------------------------------------------------

def drawHealthMeter(currentHealth):
    for i in range(currentHealth): # draw red health bars
        pygame.draw.rect(displaysurf, red,(15,5+(10*maxhealth)-i*10,20,10))
    for i in range(maxhealth): # draw the white outlines
        pygame.draw.rect(displaysurf, white,(15,5+(10*maxhealth)-i*10,20,10),1)
def terminate():
    pygame.quit(); sys.exit()

def isOutsideActiveArea(camerax,cameray,obj):
    # return False if camerax and cameray are more than a half-window length
    # beyond the edge of the window
    boundsLeftedge = camerax - winwidth
    boundsTopedge  = cameray - winheight
    boundRect = pygame.Rect(boundsLeftedge,boundsTopedge,winwidth*3,winheight*3)
    objRect = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
    return not boundRect.colliderect(objRect)

def getTextObj(basicfont,text,color,centerX,centerY):
    surf = basicfont.render(text,True,color)
    rect = surf.get_rect()
    rect.center = centerX,centerY
    return surf, rect

if __name__ == '__main__':
    main()

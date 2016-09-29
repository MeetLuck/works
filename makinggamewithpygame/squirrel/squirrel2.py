from Component2 import *

def main():
    global fpsclock, displaysurf, basicfont, l_squir_img, r_squir_img, grassImages
    pygame.init()
    fpsclock = pygame.time.Clock()
    pygame.display.set_icon(pygame.image.load('gameicon.png'))
    displaysurf = pygame.display.set_mode( (winwidth,winheight))
    basicfont = pygame.font.Font('freesansbold.ttf',32)
    pygame.display.set_caption('Squirrel eat Squirrel')
    while True:
        runGame()

def getTextObj(basicfont,text,color,centerX,centerY):
    surf = basicfont.render(text,True,color)
    rect = surf.get_rect()
    rect.center = centerX,centerY
    return surf, rect

def runGame():
    # setup variables for the start of a new game
    invulnerableMode = False # if the player is invulnerable
    invulnerableStartTime = 0 # time the player became invulnerable
    gameOverMode = False # if the player has lost
    gameOverStartTime = 0 # time the player lost
    winMode = False       # if the player has won
    # create the surfaces to hold game text
    gameOverSurf,gameOverRect = getTextObj(basicfont,'GameOver',white,winwidth/2,winheight/2)
    winSurf,winRect = getTextObj(basicfont,'You have achieved OMEGA SQUIRREL!',white,winwidth/2,winheight/2)
    winSurf2,winRect2 = getTextObj(basicfont,'Press "r" to restart',white,winwidth/2,winheight/2+30)

    # camerax and cameray are where the middle of the camera view is
    camerax,cameray = 0,0

    grassObjs = [] # stores all the grass objects in the game
    squirrelObjs = [] # stores all the non-player squirrel objects

    # stores the player object:
    playerObj = Player()
    moveLeft =  moveRight = moveDown = moveUp = False
    # start off with some random grass images on the screen
    for i in range(10):
        grassObjs.append( Grass(camerax,cameray))
        grassObjs[i].x = random.randint(0,winwidth)
        grassObjs[i].y = random.randint(0,winheight)

    while True: # main game loop
        # check if we should turn off invulnerability
        if invulnerableMode and time.time() - invulnerableStartTime > invulntime:
            invulnerableMode = False
        # move all the squirrels
        for sObj in squirrelObjs:
            # move the squirrel, and adjust for their bounce
            sObj['x'] += sObj['movex']
            sObj['y'] += sObj['movey']
            sObj['bounce'] += 1
            if sObj['bounce'] > sObj['bounceRate']:
                sObj['bounce'] = 0 # reset bounce amount
            # random chance they change direction
            if random.randint(0,99) < dirchangefreq:
                sObj['movex'] = getRandomVelocity()
                sObj['movey'] = getRandomVelocity()
                if sObj['movex'] > 0: # faces right
                    sObj['surface'] = pygame.transform.scale(r_squir_img, (sObj['width'], sObj['height']))
                else: # faces left
                    sObj['surface'] = pygame.transform.scale(l_squir_img, (sObj['width'], sObj['height']))
        # go through all the objects and see if any need to be deleted
        for i in range( len(grassObjs)-1,-1,-1):
            if isOutsideActiveArea(camerax,cameray,grassObjs[i]):
                del grassObjs[i]
        for i in range( len(squirrelObjs)-1,-1,-1):
            if isOutsideActiveArea(camerax,cameray,squirrelObjs[i]):
                del squirrelObjs[i]
        # add more grass & squirrels if we dont' have enough
        while len(grassObjs) < numgrass:
            grassObjs.append(Grass(camerax,cameray))
        while len(squirrelObjs) < numsquirrels:
            squirrelObjs.append(makeNewSquirrel(camerax,cameray))
        # adjust camerax and cameray if beyond the 'camera slack'
        if (camerax + winwidth/2) - playerObj.centerX > cameraslack:
            camerax = playerObj.centerX + cameraslack - winwidth/2
        elif playerObj.centerX - (camerax+winwidth/2) > cameraslack:
            camerax = playerObj.centerX - cameraslack - winwidth/2
        if (cameray + winheight/2) - playerObj.centerY > cameraslack:
            cameray = playerObj.centerY + cameraslack - winheight/2
        elif playerObj.centerY - (cameray+winheight) > cameraslack:
            cameray = playerObj.centerY - cameraslack - winheight/2
        # draw the green background
        displaysurf.fill(grasscolor)
        # draw all the grass object on the screen
        for gObj in grassObjs:
            gObj.draw(displaysurf,camerax,cameray)
        # draw the other squirrels
        for sObj in squirrelObjs:
            sObj['rect'] = pygame.Rect(
               (sObj['x']-camerax,
                sObj['y']-cameray-getBounceAmount(sObj['bounce'],sObj['bounceRate'], sObj['bounceheight']),
                sObj['width'],
                sObj['height']) )
            displaysurf.blit(sObj['surface'],sObj['rect'])

        #pygame.display.update()
        # draw the player squirrel
        flashIsOn = round(time.time(),1) * 10 % 2 == 1
        if not gameOverMode and not (invulnerableMode and flashIsOn):
            playerObj.draw(displaysurf,camerax,cameray)
        # draw the health meter
        drawHealthMeter(playerObj.health)
        for event in pygame.event.get():
            if event.type == QUIT: terminate()
            elif event.type == KEYDOWN:
                if event.key in (K_UP,K_w):         moveDown,moveUp = False,True
                elif event.key in (K_DOWN, K_s):    moveDown,moveUp = True, False
                elif event.key in (K_LEFT,K_a):     moveLeft,moveRight = True,False
                    if playerObj.facing == right: # change player image
                        playerObj.surface = pygame.transform.scale(l_squir_img, (playerObj.size,playerObj.size))
                        playerObj.facing = left
                elif event.key in (K_RIGHT,K_d):    moveLeft,moveRight = False,True
                    if playerObj.facing == left: # change player image
                        playerObj.surface = pygame.transform.scale(r_squir_img, (playerObj.size,playerObj.size))
                        playerObj.facing = right
                elif winMode and event.key == K_r:
                    return
            elif event.type == KEYUP:
                # stop moving the player's squirrel
                if event.key in (K_LEFT,K_a):       moveLeft = False
                elif event.key in (K_RIGHT,K_d):    moveRight = False
                elif event.key in (K_UP,K_w):       moveUp = False
                elif event.key in (K_DOWN,K_s):     moveDown = False
                elif event.key == K_ESCAPE: terminate()
        if not gameOverMode:
            # actually move the player
            if moveLeft:    playerObj.move(moveX = -moverate)
            if moveRight:   playerObj.move(moveX = +moverate)
            if moveUp:      playerObj.move(moveY = -moverate)
            if moveDown:    playerObj.move(moveY = +moverate)

            # check if the player has collided with any squirrels
            for i in range( len(squirrelObjs)-1, -1,-1):
                sqObj = squirrelObjs[i]
                if 'rect' in sqObj and playerObj.rect.colliderect(sqObj['rect']):
                    # a player/squirrel collsion has occured

                    if sqObj['width']*sqObj['height']<= playerObj.size**2:
                        # player is larger and eats the squirrel
                        playerObj.size += 1+ int( (sqObj['width']*sqObj['height'])**0.02)
                        del squirrelObjs[i]
                        if playerObj.facing == left:
                            playerObj.surface = pygame.transform.scale(l_squir_img, (playerObj.size,playerObj.size))
                        if playerObj.facing == right:
                            playerObj.surface = pygame.transform.scale(r_squir_img, (playerObj.size,playerObj.size))
                        if playerObj.size > winsize:
                            winMode = True # turn on 'win mode'
                    elif not invulnerableMode:
                        # player is smaller and takes damage
                        invulnerableMode = True
                        invulnerableStartTime = time.time()
                        playerObj.health -= 1
                        if playerObj.health == 0:
                            gameOverMode = True # turn on 'gameover mode'
                            gameOverStartTime = time.time()

        else: # game is over, show 'gameover' text
            displaysurf.blit(gameOverSurf,gameOverRect)
            if time.time() - gameOverStartTime > gameovertime:
                return # end the current game

        # check if the player has won
        if winMode:
            displaysurf.blit(winSurf,winRect)
            displaysurf.blit(winSurf2,winRect2)

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
def makeNewSquirrel(camerax, cameray):
    sq = {}
    generalSize = random.randint(5,25)
    multiplier = random.randint(1,3)
    sq['width'] = (generalSize+random.randint(0,10))*multiplier
    sq['height'] = (generalSize+random.randint(0,10))*multiplier
    sq['x'],sq['y'] = getRandomOffCameraPos(camerax,cameray,sq['width'],sq['height'])
    sq['movex'] = getRandomVelocity()
    sq['movey'] = getRandomVelocity()
    if sq['movex'] < 0: # squirrel is facing left
        sq['surface'] = pygame.transform.scale(l_squir_img,(sq['width'],sq['height']))
    else: # squirrel is facing right
        sq['surface'] = pygame.transform.scale(r_squir_img,(sq['width'],sq['height']))
    sq['bounce'] = 0
    sq['bounceRate'] = random.randint(10,18)
    sq['bounceheight'] = random.randint(10,50)
    return sq

def makeNewGrass(camerax,cameray):
    gr = {}
    gr['grassImage'] = random.randint(0,len(grassImages)-1)
    gr['width'] = grassImages[0].get_width()
    gr['height'] = grassImages[0].get_height()
    gr['x'],gr['y'] = getRandomOffCameraPos(camerax,cameray,gr['width'],gr['height'])
    gr['rect'] = pygame.Rect( (gr['x'], gr['y'],gr['width'],gr['height']) )
    return gr

def isOutsideActiveArea(camerax,cameray,obj):
    # return False if camerax and cameray are more than a half-window length
    # beyond the edge of the window
    boundsLeftedge = camerax - winwidth
    boundsTopedge  = cameray - winheight
    boundRect = pygame.Rect(boundsLeftedge,boundsTopedge,winwidth*3,winheight*3)
    if type(obj) == dict:
        objRect = pygame.Rect(obj['x'],obj['y'],obj['width'],obj['height'])
    else:
        objRect = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
    return not boundRect.colliderect(objRect)

if __name__ == '__main__':
    main()

import pygame, sys, random,time, math
from pygame.locals import *

fps = 30
winwidth,winheight = 640,480
grasscolor = 24,255,0
white = 255,255,255
red = 255,0,0

cameraslack = 90 # how far from the center the squirrel moves before moving the screen
moverate = 9 # how fast the player moves
bounceRate = 6 # how fast the player bounces(large is slower)
bounceheight = 30 # how high the player bounces
startsize = 25 # how big the player starts off
winsize =300 # how big the player needs to be to win
invulntime = 2 # how long the player is invulnerable after hit in seconds
gameovertime = 4 # how long the 'game over' text stays on the screen in seconds
maxhealth = 3 # how much health the player starts with

numgrass = 80 # number of grass objects in the active area
numsquirrels = 30 # number of squirrels in the active area
squirrelminspeed = 3 # slowest squirrel spped
squirrelmaxspeed = 7 # fastest squirrel speed
dirchangefreq = 2 # %chance of direction change per frame
left,right = 'left','right'
'''
this program has three data structures to represent the player, enemy squirrels, and grass background objects.
the data structures are dictionaries with the following keys.
keys used by all three data structures:
    'x' - the left edge coordinate of the object in the game world(not a pixel coordinate)
    'y' - the top edge coordinate of the object in the game world(not a pixel coordinate)
    'rect' - the pygame.Rect object representing where on the screen the object is located.
player data structure keys:
    'surface' - the pygame.Surface object that stores the image of the squirrel which will be drawn to the screen
    'facing' - either set to LEFT or RIGHT, stores which direction the player is facing
    'size' - the width and height of the player in pixels
    'bouce' - represents at what point in a bounce the player is in. 0 means standing(no bounce), up to bounceRate
enemy squirrel data structure keys:
    'surface' - the pygame.Surface object that stores the image of the squirrel which will be drawn to the screen
    'movex' - how many pixels per frame the squireel moves horizontally. a negative integer is moving to the left
              a positive to the right
    'movey' - how many pixels per frame the squirrel moves vertically. a negative integer is moving up, a positive
              moving down
    'width' - the width of the squirrel's image, in pixels
    'height' - the height of the squirrel's image, in pixels
    'bounce' - represents at what point in a bounce the player is in. 0 means standing(no bounce), up to bounceRate
    'bounceRate' - how quickly the squirrel bounces. a lower number means a quicker bounce.
    'bounceheight' - how high the squirrel bounces
    'grassImage' - an integer that refers to the index of the pygame.Surface object in grassImages used for this 
                   grass object
'''

def main():
    global fpsclock, displaysurf, basicfont, l_squir_img, r_squir_img, grassImages
    pygame.init()
    fpsclock = pygame.time.Clock()
    pygame.display.set_icon(pygame.image.load('gameicon.png'))
    displaysurf = pygame.display.set_mode( (winwidth,winheight))
    pygame.display.set_caption('Squirrel eat Squirrel')
    basicfont = pygame.font.Font('freesansbold.ttf',32)
    # load the image files
    l_squir_img = pygame.image.load('squirrel.png')
    r_squir_img = pygame.transform.flip(l_squir_img,True, False)
    grassImages = []
    for i in range(1,5):
        grassImages.append(pygame.image.load('grass%s.png' %i))
    while True:
        #print 'running.. Game'
        runGame()

def runGame():
    # setup variables for the start of a new game
    invulnerableMode = False # if the player is invulnerable
    invulnerableStartTime = 0 # time the player became invulnerable
    gameOverMode = False # if the player has lost
    gameOverStartTime = 0 # time the player lost
    winMode = False       # if the player has won
    # create the surfaces to hold game text
    gameOverSurf = basicfont.render('Game Over', True, white)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.center = winwidth/2, winheight/2

    winSurf = basicfont.render('You have achieved OMEGA SQUIRREL!', True, white)
    winRect = winSurf.get_rect()
    winRect.center = winwidth/2, winheight/2
    winSurf2 = basicfont.render('(Press "r" to restart.)', True,white)
    winRect2 = winSurf2.get_rect()
    winRect2.center = winwidth/2, winheight/2 + 30

    # camerax and cameray are where the middle of the camera view is
    camerax,cameray = 0,0

    grassObjs = [] # stores all the grass objects in the game
    squirrelObjs = [] # stores all the non-player squirrel objects

    # stores the player object:
    playerObj = {'surface': pygame.transform.scale(l_squir_img,(startsize, startsize)),
                 'facing': left,
                 'size' : startsize,
                 'x': winwidth/2,
                 'y': winheight/2,
                 'bounce':0,
                 'health': maxhealth }
    moveLeft =  moveRight = moveDown = moveUp = False
    # start off with some random grass images on the screen
    for i in range(10):
        grassObjs.append( makeNewGrass(camerax,cameray))
        grassObjs[i]['x'] = random.randint(0,winwidth)
        grassObjs[i]['y'] = random.randint(0,winheight)

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
            grassObjs.append(makeNewGrass(camerax,cameray))
        while len(squirrelObjs) < numsquirrels:
            squirrelObjs.append(makeNewSquirrel(camerax,cameray))
        # adjust camerax and cameray if beyond the 'camera slack'
        playerCenterX = playerObj['x'] + int(playerObj['size']/2)
        playerCenterY = playerObj['y'] + int(playerObj['size']/2)
        if (camerax + winwidth/2) - playerCenterX > cameraslack:
            camerax = playerCenterX + cameraslack - winwidth/2
        elif playerCenterX - (camerax+winwidth/2) > cameraslack:
            camerax = playerCenterX - cameraslack - winwidth/2
        if (cameray + winheight/2) - playerCenterY > cameraslack:
            cameray = playerCenterY + cameraslack - winheight/2
        elif playerCenterY - (cameray+winheight) > cameraslack:
            cameray = playerCenterY - cameraslack - winheight/2
        # draw the green background
        displaysurf.fill(grasscolor)
        # draw all the grass object on the screen
        #print 'all the grass'
        for gObj in grassObjs:
            gRect = pygame.Rect( (gObj['x']-camerax, gObj['y']-cameray, gObj['width'], gObj['height']) )
            displaysurf.blit( grassImages[gObj['grassImage']], gRect)
        #pygame.display.update()
        # draw the other squirrels
        #print 'draw the other squirrels'
        for sObj in squirrelObjs:
            sObj['rect'] = pygame.Rect(
               (sObj['x']-camerax,
                sObj['y']-cameray-getBounceAmount(sObj['bounce'],sObj['bounceRate'], sObj['bounceheight']),
                sObj['width'],
                sObj['height']) )
            displaysurf.blit(sObj['surface'],sObj['rect'])

        #pygame.display.update()
        # draw the player squirrel
        #print 'draw the player'
        flashIsOn = round(time.time(),1) * 10 % 2 == 1
        if not gameOverMode and not (invulnerableMode and flashIsOn):
            playerObj['rect'] = pygame.Rect(
                    (playerObj['x']-camerax,
                     playerObj['y']-cameray-getBounceAmount(playerObj['bounce'], bounceRate, bounceheight),
                     playerObj['size'],
                     playerObj['size']) )
            displaysurf.blit( playerObj['surface'], playerObj['rect'] )
        pygame.display.update()
        # draw the health meter
        #print 'draw the health meter'
        drawHealthMeter(playerObj['health'])
        for event in pygame.event.get():
            if event.type == QUIT: terminate()
            elif event.type == KEYDOWN:
                if event.key in (K_UP,K_w):
                    moveDown,moveUp = False,True
                elif event.key in (K_DOWN, K_s):
                    moveDown,moveUp = True, False
                elif event.key in (K_LEFT,K_a):
                    moveLeft,moveRight = True,False
                    if playerObj['facing'] == right: # change player image
                        playerObj['surface'] = pygame.transform.scale(l_squir_img, (playerObj['size'],playerObj['size']))
                    playerObj['facing'] = left
                elif event.key in (K_RIGHT,K_d):
                    moveLeft,moveRight = False,True
                    if playerObj['facing'] == left: # change player image
                        playerObj['surface'] = pygame.transform.scale(r_squir_img, (playerObj['size'],playerObj['size']))
                    playerObj['facing'] = right
                elif winMode and event.key == K_r:
                    return
            elif event.type == KEYUP:
                # stop moving the player's squirrel
                if event.key in (K_LEFT,K_a):
                    moveLeft = False
                elif event.key in (K_RIGHT,K_d):
                    moveRight = False
                elif event.key in (K_UP,K_w):
                    moveUp = False
                elif event.key in (K_DOWN,K_s):
                    moveDown = False
                elif event.key == K_ESCAPE: terminate()
        if not gameOverMode:
            # actually move the player
            if moveLeft:    playerObj['x']  +=  -moverate
            if moveRight:   playerObj['x']  +=  +moverate
            if moveUp:      playerObj['y']  +=  -moverate
            if moveDown:    playerObj['y']  +=  +moverate
            if (moveLeft or moveRight or moveUp or moveDown) or playerObj['bounce'] != 0:
                playerObj['bounce'] += 1
            if playerObj['bounce'] > bounceRate:
                playerObj['bounce'] = 0 # reset bounce amount

            # check if the player has collided with any squirrels
            for i in range( len(squirrelObjs)-1, -1,-1):
                sqObj = squirrelObjs[i]
                if 'rect' in sqObj and playerObj['rect'].colliderect(sqObj['rect']):
                    # a player/squirrel collsion has occured

                    if sqObj['width']*sqObj['height']<= playerObj['size']**2:
                        # player is larger and eats the squirrel
                        playerObj['size'] += 1+ int( (sqObj['width']*sqObj['height'])**0.02)
                        del squirrelObjs[i]
                        if playerObj['facing']==left:
                            playerObj['surface'] = pygame.transform.scale(l_squir_img, (playerObj['size'],playerObj['size']))
                        if playerObj['facing']==right:
                            playerObj['surface'] = pygame.transform.scale(r_squir_img, (playerObj['size'],playerObj['size']))
                        if playerObj['size'] > winsize:
                            winMode = True # turn on 'win mode'
                    elif not invulnerableMode:
                        # player is smaller and takes damage
                        invulnerableMode = True
                        invulnerableStartTime = time.time()
                        playerObj['health'] -= 1
                        if playerObj['health'] == 0:
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
def getBounceAmount(currentBounce,bounceRate,bounceHeight):
    # return he number of pixels to offset based on the bounce
    # larger bounceRate means a slower bounce
    # larger bounceheight means a higher bounce
    # currentBounce will always be less than bounceRate
    return int( math.sin( (math.pi/float(bounceRate)) * currentBounce ) * bounceHeight )
def getRandomVelocity():
    speed = random.randint( squirrelminspeed,squirrelmaxspeed )
    if random.randint(0,1)==0: return speed
    else: return -speed
def getRandomOffCameraPos(camerax,cameray,objWidth,objHeight):
    # create a Rect of the camera view
    cameraRect = pygame.Rect( camerax, cameray, winwidth, winheight)
    while True:
        x = random.randint(camerax - winwidth, camerax+2*winwidth)
        y = random.randint(cameray - winheight, cameray+2*winheight)
        # create a rect object with the random coordinates and use colliderect()
        # to make sure the right edge isn't in the camera view
        objRect = pygame.Rect(x,y,objWidth,objHeight)
        if not objRect.colliderect(cameraRect):
            return x,y
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
    objRect = pygame.Rect(obj['x'],obj['y'],obj['width'],obj['height'])
    return not boundRect.colliderect(objRect)

if __name__ == '__main__':
    main()

















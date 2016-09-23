import pygame, sys, time, random
from pygame.locals import *
from constants import *


def main():
    global fpsclock, displaysurf, basicfont, bigfont
    pygame.init()
    fpsclock = pygame.time.Clock()
    displaysurf = pygame.display.set_mode( (width,height))
    basicfont = pygame.font.Font('freesansbold.ttf',18)
    bigfont = pygame.font.Font('freesansbold.ttf',100)
    pygame.display.set_caption('Tetromino')
    showTextScreen('Tetromino')
    while True:
        if random.randint(0,1) == 0:
            pygame.mixer.music.load('tetrisb.mid')
        else:
            pygame.mixer.music.load('tetrisc.mid')
        pygame.mixer.music.play(-1,0.0)
        runGame()
        pygame.mixer.music.stop()
        showTextScreen('Game Over')

def runGame():
    # setup variables for the start of the game
    board = getBlankBoard()
    lastmovedowntime = lastmovesidewaystime = lastfalltime = time.time()
    movingdown = movingleft = movingright = False
    score = 0
    level, fallfreq = calculateLevelAndFallFreq(score)
    fallingpiece = getNewPiece()
    nextpiece = getNewPiece()

    while True:
        if fallingpiece == None:
            # no falling piece in play, so start a new piece at the top
            fallingpiece = nextpiece
            nextpiece = getNewPiece()
            lastfalltime = time.time() # reset last fall time

            if not isValidPosition(board,fallingpiece):
                return # can't fit a new piece on the board, so game over
        checkForQuit()
        for e in pygame.event.get():
            if e.type == KEYUP:
                if   e.key == K_LEFT:    movingleft = False
                elif e.key == K_RIGHT:   movingright = False
                elif e.key == K_DOWN:    movingdown = False
            elif e.type == KEYDOWN: # moving sideways
                if e.key == K_LEFT and isValidPosition(board,fallingpiece,adjX=-1):
                    fallingpiece['x'] += -1
                    movingleft = True
                    movingright = False
                    #lastmovesidewaystime = time.time()
                elif e.key == K_RIGHT and isValidPosition(board,fallingpiece,adjX=1):
                    fallingpiece['x'] += +1
                    movingleft = True
                    movingright = False
                    #lastmovesidewaystime = time.time()
                # rotate the piece if there is room to rotate
                elif e.key == K_UP and isValidPosition(board,fallingpiece,adjX=1):
                    fallingpiece['rotation'] = (fallingpiece['rotation']+1)%len(pieces[fallingpiece['shape']])
                    if not isValidPosition(board,fallingpiece):
                        fallingpiece['rotation'] = (fallingpiece['rotation']-1)%len(pieces[fallingpiece['shape']])
                # move the piece fall faster with the down key
                elif e.key == K_DOWN:
                    movingdown = True
                    if isValidPosition(board,fallingpiece,adjY=1):
                        fallingpiece['y'] += +1
                    lastmovingdowntime = time.time()
                # move the current piece all the way down
                elif e.key == K_SPACE:
                    movingdown = movingleft = movingright = False
                    for i in range(1, boardheight):
                        if not isValidPosition(board,fallingpiece,adjY=i):
                            break
                        fallingpiece['y'] += i - 1
                
                # handle moving the piece because of user input
                if movingleft and isValidPosition(board,fallingpiece,adjX=-1):
                    fallingpiece['x'] -= 1
                elif movingright and isValidPosition(board,fallingpiece,adjX=1):
                    fallingpiece['x'] += 1
                #lastmovesidewaystime = time.time()
                if movingdown and time.time() - lastmovedowntime > movedownfreq and isValidPosition(board,fallingpiece,adjY=1):
                    fallingpiece['y'] += 1
                    lastmovedowntime = time.time()

                # let the piece fall if it is time to fall
                if time.time() - lastfalltime > fallfreq:
                    # see if the piece has landed
                    if not isValidPosition(board,fallingpiece,adjY=1):
                        # falling piece has landed, set it on the board
                        addToBoard(board, fallingpiece)
                        score += removeCompleteLines(board)
                        level, fallfreq = calculateLevelAndFallFreq(score)
                        fallingpiece = None
                    else:
                        # piece did not land, just move the piece down
                        fallingpiece['y'] += 1
                        lastfalltime = time.time()
                # drawing everything on the screen
                displaysurf.fill(bgcolor)
                drawBoard(board)
                drawStatus(score,level)
                drawNextPiece(nextpiece)
                if fallingpiece != None:
                    drawPiece(fallingpiece)
                pygame.display.update()
                fpsclock.tick(fps)

def makeTextObjs(text,font,color):
    surf = font.render(text,True,color)
    return surf, surf.get_rect()
def terminate():
    pygame.quit(); sys.exit()
def checkForKeyPress():
    # go through event queue looking for a KEYUP event
    # grab KEYDOWN events to remove them from the event queue
    checkForQuit()
    for e in pygame.event.get([KEYDOWN,KEYUP]):
        if e.type == KEYDOWN:
            continue
        return e.key
    return None
def showTextScreen(text):
    # displays large text in the center of the screen until a key is pressed
    # draw the text drop shadow
    titlesurf,titlerect = makeTextObjs(text,bigfont,textshadowcolor)
    titlerect.center = width/2, height/2
    displaysurf.blit(titlesurf,titlerect)
    # draw the text
    titlesurf,tilerect = makeTextObjs(text,bigfont,textcolor)
    titlerect.center = width/2-3, height/2-3
    displaysurf.blit(titlesurf,titlerect)
    # draw the additional 'Press a key to display.' text
    presskeysurf, presskeyrect = makeTextObjs('Press a key to play.',basicfont,textcolor)
    presskeyrect.center = width/2, height/2 + 100
    displaysurf.blit(presskeysurf,presskeyrect)
    while checkForKeyPress == None:
        pygame.display.update()
        fpsclock.tick()
def checkForQuit():
    for e in pygame.event.get(QUIT): # get all the QUIT events
        terminate()
    for e in pygame.event.get(KEYUP): # get all the KEYUP events
        if e.key == K_ESCAPE:
            terminate()
        pygame.event.post(e)
def calculateLevelAndFallFreq(score):
    # based on the score, return the level the player is on and how many seconds pass
    # until a falling piece falls one space
    level = int(score/10) + 1
    fallfreq = 0.27 - level*0.02
    return level,fallfreq
def getNewPiece():
    # return a random new piece in a random rotation and color
    shape = random.choice( list(pieces.keys()))
    newpiece = {'shape':shape,
                'rotation': random.randint(0, len(pieces[shape])-1),
                'x': int(boardwidth/2) - int(templatewidth/2),
                'y': -2, # start it above the board(i.e. less than 0)
                'color': random.randint(0,len(colors)-1) }
    return newpiece
def addToBoard(board,piece):
    # fill in the board based on piece's location, shape, and rotation
    for x in range(templatewidth):
        for y in range(templateheight):
            if pieces[piece['shape']][piece['rotation']][y][x] != blank:
                board[x+piece['x']][y+piece['y']] = piece['color']

def getBlankBoard():
    # create and return a new blank board data structure
    board = []
    for i in range(boardwidth):
        board.append( [blank]*boardheight )
    return board

def isOnBoard(x,y):
    return 0 <= x < boardwidth and y < boardheight

def isValidPosition(board,piece,adjX=0,adjY=0):
    # return True if the piece is within the board and not colliding
    for x in range(templatewidth):
        for y in range(templateheight):
            isaboveboard = y + piece['y'] + adjY < 0
            if isaboveboard or pieces[piece['shape']][piece['rotation']][y][x] == blank:
                continue
            if not isOnBoard(x+piece['x']+adjX,y+piece['y']+adjY):
                return False
            if board[x+piece['x']+adjX][y+piece['y']+adjY] != blank:
                return False
    return True

def isCompleteLine(board,y):
    # return True if the line filled with boxes with no gaps
    for x in range(boardwidth):
        if board[x][y] == blank:
            return False
    return True

def removeCompleteLines(board):
    # remove any completed lines on the board, move everything above them down, and
    # return the number of complete lines.
    numlinesremoved = 0
    y = boardheight - 1 # start y at the bottom of the board
    while y>=0:
        if isCompleteLine(board,y):
            # remove the line and pull boxes down by one line
            for pulldownY in range(y,0,-1):
                for x in range(boardwidth):
                    board[x][pulldownY] = board[x][pulldownY-1]
            # set very top line to blank
            for x in range(boardwidth):
                board[x][0] = blank
            numlinesremoved += 1
            # note on the next iteration of the loop, y is the same
            # this is so that if the line that was pulled down is also
            # complete, it will be removed
        else:
            y -= 1
    return numlinesremoved

def converToPixelCoords(boxx,boxy):
    # convert the given x,y coordinates of the board to the screen coordinates
    return (xmargin + boxx*boxsize),(topmargin+boxy*boxsize)
def drawBox(boxx,boxy,color,pixelx=None,pixely=None):
    # draw a single box (each tetromino piece has four boxes) at x,y coordinates on the board.
    # Or, if pixelx & pixely are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the 'Next' piece).
    if color == blank: return
    if (pixelx,pixely) == (None,None):
        pixelx,pixely = converToPixelCoords(boxx,boxy)
    pygame.draw.rect(displaysurf,colors[color],(pixelx+1,pixely+1,boxsize-1,boxsize-1))
    pygame.draw.rect(displaysurf,lightcolors[color],(pixelx+1,pixely+1,boxsize-4,boxsize-4))

def drawBoard(board):
    # draw the border around the board
    pygame.draw.rect(displaysurf, bordercolor,(xmargin-3,topmargin-7,boardwidth*boxsize+8,boardheight*boxsize+8),5)
    # fill the background of the board
    pygame.draw.rect(displaysurf, bgcolor,(xmargin,topmargin,boardwidth*boxsize,boardheight*boxsize) )
    # draw the individual boxes on the board
    for x in range(boardwidth):
        for y in range(boardheight):
            drawBox(x,y,board[x][y])

def drawStatus(score,level):
    surf = basicfont.render('Score:%s' %score,True,textcolor)
    rect = surf.get_rect()
    rect.topleft = width-150,20
    displaysurf.blit(surf,rect)

def drawPiece(piece,pixelx=None,pixely=None):
    shapetodraw = pieces[piece['shape']][piece['rotation']]
    if (pixelx,pixely) == (None,None):
        pixelx,pixely = converToPixelCoords(piece['x'],piece['y'])
    # draw each of the boxes that make up the piece
    for x in range(templatewidth):
        for y in range(templateheight):
            if shapetodraw[y][x] != blank:
                drawBox(None,None,piece['color'],pixelx + x*boxsize, pixely + y*boxsize)

def drawNextPiece(piece):
    surf = basicfont.render('Next: ', True, textcolor)
    rect = surf.get_rect()
    displaysurf.blit(surf,rect)
    drawPiece(piece,pixelx=width-120,pixely=100)

if __name__ == '__main__':
    main()




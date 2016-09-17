import pygame,sys,random
from pygame.locals import *
from constants import *

def main():
    global fpsclock, surface, basicfont, reset_surf, reset_rect,new_surf,new_rect,\
           solve_surfe,solve_rect
    pygame.init()
    surface = pygame.display.set_mode( resolution )
    pygame.display.set_caption('Slide Puzzle')
    basicfont = pygame.font.Font('freesansbold.ttf',basicfontsize)
    # store the option buttons and their rectangles in options
    reset_surf,reset_rect = makeText('Reset', textcolor, tilecolor, width-120, height-90)
    new_surf, new_rect = makeText('New Game', textcolor, tilecolor, width-120,height-60)
    solve_surf,solve_rect = makeText('Solve', textcolor, tilecolor, width-120, height-30)

    mainboard, solutionSeq = generateNewPuzzle(80)
    solvedboard = getStartingBoard() # a solved board is the same as the board in a start state
    allmoves = [] # list of moves made from the solved configuration

    while True: # main game loop
        slideTo = None # the direction, if any, a tile should slide
        msg = '' # contains the message to show in the upper left corner
        if mainboard == solvedboard:
            msg = 'Solved'
        drawBoard(mainboard,msg)

        checkForQuit()
        for e in pygame.event.get():
            if e.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainboard, e.pos[0], e.pos[1])
                if (spotx,spoty) == (None,None):
                    # check if the user clicked on an option button
                    if reset_rect.collidepoint(e.pos):
                        resetAnimation(mainboard, allmoves) # clicked on Reset button
                        allmoves = []
                    elif new_rect.collidepoint(e.pos):
                        mainboard, solutionSeq = generateNewPuzzle(80) # clicked on New Game button
                        allmoves = []
                    elif solve_rect.collidepoint(e.pos):
                        resetAnimation(mainboard,solutionSeq+allmoves) # clicked on Solve button
                        allmoves = []
                else: # check if the clicked tile was next to the blank spot
                    blankx,blanky = getBlankPosition(mainboard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = left
                    elif spotx == blankx-1 and spoty==balnky:
                        slideTo = right
                    elif spotx == blankx and spoty==blanky + 1:
                        slideTo = up
                    elif spotx == balnkx and spoty == blanky -1:
                        slideTo = down
            elif e.type == KEYUP:
                # check if the user pressed a key to slide a tile
                if e.key in (k_LEFT,K_a) and isValidMove(mainboard,left):
                    slideTo = left
                elif e.key in (K_RIGHT,K_d) and isValidMove(mainboard,right):
                    slideTo = right
                elif e.key in (K_UP,K_w) and isValidMove(mainboard,up):
                    slideTo = up
                elif e.key in (K_DOWN,K_s) and isValidMove(mainboard,down):
                    slideTo = down
        if slideTo:
            # show slide on screen
            slideAnimation(mainboard,slideTo,'Click tile or press arrow keys to slide.',8)
            makeMove(mainboard,slideTo)
            allmoves.append(slideTo) # record the slide
        pygame.display.update()
        fpsclock.tick(fps)

def terminate():
    pygame.quit()
    sys.exit()
def checkForQuit():
    for e in pygame.event.get(QUIT): # get all the QUIT events
        terminate()
    for e in pygame.event.get(KEYUP):
        if e.key == K_ESCAPE:
            terminate()
        pygame.event.post(event) # put the other KEYUP event objects back
def getStartingBoard():
    # return a board data structure with tiles in the solved state.
    # e.g., if boardwidth and boardheight are both 3, this function
    # returns [ [1,4,7],[2,5,8],[3,6,None] ] 
    counter = 1
    board = []
    for x in range(boardwidth):
        column = []
        for y in range(boardheight):
            column.append(counter)
            counter += boardwidth
        board.append(column)
        counter -= boardwidth * (boardheight-1) + boardwidth - 1
    board[boardwidth-1][boardheight-1] = None
    return board

def getBlankPosition(board):
    # return the x and y of board coordinates of the blank space
    for x in range(boardwith):
        for y in range(boardheight):
            if board[x][y] == None:
                return (x,y)
def makeMove(board,move):
    blankx,blanky = getBlankPosition(board)
    if move == up:
        board[blankx][blanky], board[blankx][blanky+1] = board[blankx][blanky+1],board[blankx][blanky]
    elif move == down:
        board[blankx][blanky], board[blankx][blanky-1] = board[blankx][blanky-1],board[blankx][blanky]
    elif move == left:
        board[blankx][blanky], board[blankx+1][blanky] = board[blankx+1][blanky],board[blankx][blanky]
    elif move == right:
        board[blankx][blanky], board[blankx-1][blanky] = board[blankx-1][blanky],board[blankx][blanky]
def isValidMove(board,move):
    blankx,blanky = getBlankPosition(board)
    return (move == up and blanky != len(board[0])-1) or \
           (move == down and blanky != 0) or \
           (move == left and blanky != len(board)-1) or \
           (move == right and blanky != 0)
def getRandomMove(board,lastMove=None):
    # start with a full list of all four moves
    validMoves = [ up,down,left,right ]
    # remove moves from the list as they are disqualified
    if lastMove==up or not isValideMove(board,down):
        validMoves.remove(down)
    if lastMove==down or not isValideMove(board,up):
        validMoves.remove(up)
    if lastMove==left or not isValideMove(board,right):
        validMoves.remove(right)
    if lastMove==right or not isValideMove(board,left):
        validMoves.remove(left)
    # return a random move from the list of remaining moves
    return random.choice(validMoves)
def getLeftTopOfTile(tileX,tileY):
    left = xmargin + (tileX*tilesize) + (tileX-1)
    top = ymargin + (tileY*tilesize) + (tileY-1)
    return (left,top)
def getSpotClicked(board,x,y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left,top = getLeftTopOfTile(tileX,tileY)
            tileRect = pygame.Rect(left,top,tilesize,tilesize)
            if tileRect.collidepoint(x,y):
                return (tileX,tileY)
    return (None,None)

def drawTile(tilex,tiley,number, adjx=0,adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and ajdy)
    left,top = getLeftTopOfTile(tilex,tiley)
    textsurf = basicfont.render( str(number), True, textcolor)
    textrect = textsurf.get_rect()
    textrect.center = left + int(tilesize/2) + adjx, top + int(tilesize/2) + adjy
    surface.blit(textsurf, textrect)

def makeText(text,color,bgcolor,top,left):
    # create the surface and rect objects for some text
    textsurf = basicfont.render(text,True,color,bgcolor)
    textrect = textsurf.get_rect()
    textrect.topleft = (top,left)
    return (textsurf, textrect)

def drawBoard(board,message):
    surface.fill(bgcolor)
    if message:
        textsurf,textrect = makeText(message,messagecolor,bgcolor,5,5)
        surface.blit(textsurf,textrect)
    for tilex in range(len(board)):
        for tiley in range( len(board[0]) ):
            if board[tilex][tiley]:
                drawTile(tilex,tiley,board[tilex][tiley])
    left,top = getLeftTopOfTile(0,0)
    iwidth = boardwith * tilesize
    iheight = boardheight * tilesize
    pygame.draw.rect(surface,boardcolor,(left-5,top-5,iwidth+11,iheight+11),4)
    surface.blit(reset_surf, reset_rect)
    surface.blit(new_surf, new_rect)
    surface.blit(solve_surf, solve_rect)

def slideAnimation(board,direction,message,animationSpeed):
    blankx,blanky = getBlankPosition(board)
    if direction == up:
        movex, movey = blankx, blanky+1
    elif direction == down:
        movex, movey = blankx, blanky-1
    elif direction == left:
        movex, movey = blankx+1, blanky
    elif direction == right:
        movex, movey = blankx-1, blanky
    # prepare the base surface
    drawBoard(board,message)
    basesurf = surface.copy()
    # drwo a blank space over the moving tile on the basesurface
    moveleft,movetop = getLeftTopOfTile(movex,movey)
    pygame.draw.rect(basesurf,bgcolor,(moveleft,movetop,tilesize,tilesize))
    for i in range(0, tilesize, animationSpeed):
        # animae the tile sliding over
        checkForQuit()
        surface.blit(basesurf,(0,0))
        if direction == up:
            drawTile(movex,movey,board[movex][movey],0,-i)
        if direction == down:
            drawTile(movex,movey,board[movex][movey],0,+i)
        if direction == left:
            drawTile(movex,movey,board[movex][movey],-i,0)
        if direction == right:
            drawTile(movex,movey,board[movex][movey],+i,0)
        pygame.display.update()
        fpsclock.tick(fps)
def generateNewPuzzle(numSlides):
    # from a starting configuration, make numSlides number of moves
    # and animate these moves
    seq = []
    board = getStartingBoard()
    drawBoard(board,'')
    pygame.display.update()
    pygame.time.wait(500) 
    lastmove = None
    for i in range(numSlides):
        move = getRandomMove(board,lastMove)
        slideAnimation(board,move,'Generating new puzzle...', int(tilesize/3))
        makeMove(board,move)
        seq.append(move)
        lastmove = move
    return (board,seq)

def resetAnimation(board, allmoves):
    # make all of the moves in reverse
    revallmoves = allmoves[:]
    revallmoves.reverse()
    for move in revallmoves:
        if move == up:
            oppositemove = down
        elif move == down:
            oppositemove = up
        elif move == left:
            oppositemove = right
        elif move == right:
            oppositemove = left
        slideAnimation(board,oppositemove,'',int(tilesize/2))
        makeMove(board,oppositemove)

if __name__ == '__main__':
    main()















import pygame,sys,random, itertools
from pygame.locals import *
from constants import *

def main():
    global fpsclock, surface, basicfont, reset_surf, reset_rect,new_surf,new_rect,\
           solve_surf,solve_rect
    pygame.init()
    fpsclock = pygame.time.Clock()
    surface = pygame.display.set_mode( resolution )
    pygame.display.set_caption('Slide Puzzle')
    basicfont = pygame.font.Font('freesansbold.ttf',basicfontsize)
    # store the option buttons and their rectangles in options
    new_surf, new_rect = makeText('New Game', textcolor, tilecolor, width-120,height-60)
    solve_surf,solve_rect = makeText('Solve', textcolor, tilecolor, width-120, height-30)

    mainboard, solutionSeq = generateNewPuzzle(80)
    solvedboard = getStartingBoard() # a solved board is the same as the board in a start state
    #allmoves = [] # list of moves made from the solved configuration

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
                    if new_rect.collidepoint(e.pos):
                        mainboard, solutionSeq = generateNewPuzzle(80) # clicked on New Game button
                        #allmoves = []
                    elif solve_rect.collidepoint(e.pos):
                        #resetAnimation(mainboard,solutionSeq+allmoves) # clicked on Solve button
                        #allmoves = []
                        pass
                else: # check if the clicked tile was next to the blank spot
                    blankx,blanky = getBlankPosition(mainboard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = left
                    elif spotx == blankx-1 and spoty==blanky:
                        slideTo = right
                    elif spotx == blankx and spoty==blanky + 1:
                        slideTo = up
                    elif spotx == blankx and spoty == blanky -1:
                        slideTo = down
            elif e.type == KEYUP:
                # check if the user pressed a key to slide a tile
                if e.key in (K_LEFT,K_a) and isValidMove(mainboard,left):
                    slideTo = left
                elif e.key in (K_RIGHT,K_d) and isValidMove(mainboard,right):
                    slideTo = right
                elif e.key in (K_UP,K_w) and isValidMove(mainboard,up):
                    slideTo = up
                elif e.key in (K_DOWN,K_s) and isValidMove(mainboard,down):
                    slideTo = down
        if slideTo:
            # show slide on screen
            #slideAnimation(mainboard,slideTo,'Click tile or press arrow keys to slide.',8)
            makeMove(mainboard,slideTo)
            #allmoves.append(slideTo) # record the slide
        pygame.display.update()
        fpsclock.tick(fps)

#------------------- helper functions ----------------------------------------------------------------

def terminate():
    pygame.quit()
    sys.exit()
def checkForQuit():
    for e in pygame.event.get(QUIT): # get all the QUIT events
        terminate()
    for e in pygame.event.get(KEYUP):
        if e.key == K_ESCAPE:
            terminate()
        pygame.event.post(e) # put the other KEYUP event objects back
def getStartingBoard():
    # return a board data structure with tiles in the solved state.
    # e.g., if boardwidth and boardheight are both 3, this function
    # returns board = [ [1,4,7],[2,5,8],[3,6,None] ]
    # board[row][col] == board[x][y]
    # board[0][0],board[1][0],board[2][0] = 1,2,3
    li = range(1,boardwidth*boardheight)
    iterlist = iter(li)
    niters = [iterlist] * boardwidth  # [iterator obj,same obj ,same obj,....] 
    itboard = itertools.izip_longest(*niters,fillvalue=None)
    return map(list,zip(*itboard))

def getBlankPosition(board):
    # return the x and y of board coordinates of the blank space
    for x in range(boardwidth):
        for y in range(boardheight):
            if board[x][y] == blank:
                return (x,y)

def makeMove(board,move): # up,down,left,right
    blankx,blanky = getBlankPosition(board)
    if move == up:
        board[blankx][blanky], board[blankx][blanky+1]  =  board[blankx][blanky+1], board[blankx][blanky]
    elif move == down:
        board[blankx][blanky], board[blankx][blanky-1]  =  board[blankx][blanky-1], board[blankx][blanky]
    elif move == left:
        board[blankx][blanky], board[blankx+1][blanky]  =  board[blankx+1][blanky], board[blankx][blanky]
    elif move == right:
        board[blankx][blanky], board[blankx-1][blanky]  =  board[blankx-1][blanky], board[blankx][blanky]
def isValidMove(board,move):
    blankx,blanky = getBlankPosition(board)
    return (move == up and blanky != len(board[0])-1) or \
           (move == down and blanky != 0) or \
           (move == left and blankx != len(board)-1) or \
           (move == right and blankx != 0)
def getRandomMove(board,lastMove=None):
    # start with a full list of all four moves
    validMoves = [up,down,left,right]
    # remove moves from the list as they are disqualified
    if lastMove == up or not isValidMove(board,down):
        validMoves.remove(down)   # move from DOWN
    if lastMove == down or not isValidMove(board,up):
        validMoves.remove(up)     # move from UP
    if lastMove == left or not isValidMove(board,right):
        validMoves.remove(right)  # move from RIGHT
    if lastMove == right or not isValidMove(board,left):
        validMoves.remove(left)   # move from LEFT
    # return a random move from the list of remaining moves
    return random.choice(validMoves)
def convertToPixelPos(boardX,boardY):
    left = xmargin + (boardX*tilesize) + (boardX-1)
    top  = ymargin + (boardY*tilesize) + (boardY-1)
    return (left,top)
def convertToBoardPos(board,mouseX,mouseY):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for boardX in range(len(board)):
        for boardY in range(len(board[0])):
            left,top = convertToPixelPos(boardX,boardY)
            tileRect = pygame.Rect(left,top,tilesize,tilesize)
            if tileRect.collidepoint(mouseX,mouseY):
                return (boardX,boardY)
    return (None,None)

def drawTile(boardX,boardY,number, adjx=0,adjy=0):
    # draw a tile at board coordinates boardX and boardY, optionally a few
    # pixels over (determined by adjx and ajdy)
    left,top = convertToPixelPos(boardX,boardY)
    pygame.draw.rect(surface, tilecolor, (left + adjx, top + adjy, tilesize, tilesize))
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
    for boardX in range(len(board)):
        for boardY in range( len(board[0]) ):
            if board[boardX][boardY]:
                drawTile(boardX,boardY,board[boardX][boardY])
    left,top = convertToPixelPos(0,0)
    borderwidth = boardwidth * tilesize
    borderheight = boardheight * tilesize
    pygame.draw.rect(surface,bordercolor,(left-5,top-5,borderwidth+11,borderheight+11),4)
    surface.blit(new_surf, new_rect)
    surface.blit(solve_surf, solve_rect)

def generateNewPuzzle(numSlides):
    # from a starting configuration, make numSlides number of moves
    # and animate these moves
    sequence = []
    board = getStartingBoard()
    drawBoard(board,'')
    pygame.display.update()
    pygame.time.wait(500) 
    lastmove = None
    for i in range(numSlides):
        move = getRandomMove(board,lastmove)
        #slideAnimation(board,move,'Generating new puzzle...', int(tilesize/3))
        makeMove(board,move)
        sequence.append(move)
        lastmove = move
    return (board,sequence)

if __name__ == '__main__':
    main()















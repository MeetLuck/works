import pygame, sys, random, winsound
from pygame.locals import *
from itertools import product
# resolution, boardwith, boardhight, colors,...
from memorypuzzleconstants import *
class Box:
    def __init__(self,*arg):
        # arg is tuple
        if type(arg[0]) is tuple:  # isinstance(name, tuple)
            # arg = ( tuple, ) = ( (x,y), )
            self.x,self.y = arg[0]
        else: # arg = (x,y)
            self.x, self.y = arg

def main():
    global fpsclock, surface
    pygame.init()
    fpsclock = pygame.time.Clock()
    surface = pygame.display.set_mode(resolution)
    pygame.display.set_caption('Memory Game')

    mainboard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)
    surface.fill(bgcolor)
    startGameAnimation(mainboard)

    mousex,mousey = 0,0  # mouse point 
    firstselection = None  # (x,y) of the first box clicked

    print 'entering mainloop'

    while True: # main loop
        mouseclicked = False
        surface.fill(bgcolor)
        drawBoard(mainboard, revealedBoxes)

        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                pygame.quit(); sys.exit()
            elif e.type == MOUSEMOTION:
                mousex,mousey = e.pos
            elif e.type == MOUSEBUTTONUP:
                mousex,mousey = e.pos
                mouseclicked = True

        # get box coordinate of current mouse point
        box = getBoxAtPixel(mousex,mousey)

        if box.x == None or box.y == None: continue 
        #-------------- mouse is over a box -----------------------------------------------------------
#       if box.x != None and box.y != None: # check if the mouse is currently over a box.
        if not revealedBoxes[box.x][box.y] and not mouseclicked:
            drawHightlightBox(box)

        if not revealedBoxes[box.x][box.y] and mouseclicked:
            winsound.Beep(500,50)
            revealBoxesAnimation(mainboard, [(box.x,box.y)])

            # set the box as revealed whether icon1 == icon2 or not
            # set the box as revelaed whether first selection or second selection
            revealedBoxes[box.x][box.y] = True

            # the current box was first box clicked
            if firstselection == None:
                firstselection = box

            # the current box was the second box clicked
            else:
            # check if there is a match between the two icons
            # ---> second box clicked ------------------------------------------------------------------
                icon1shape,icon1color = getShapeAndColor(mainboard,firstselection)
                icon2shape,icon2color = getShapeAndColor(mainboard,box)

                if icon1shape != icon2shape or icon1color != icon2color:
                    # icons don't match. Re-cover up both selections
                    # set reaveledBoxes(first selction) = False & reaveledBoxes(second selction) = False
                    pygame.time.wait(200) # 1000 msec = 1 sec
                    coverBoxesAnimation(mainboard, [(firstselection.x,firstselection.y),(box.x,box.y)])
                    revealedBoxes[firstselection.x][firstselection.y] = False
                    revealedBoxes[box.x][box.y] = False
                elif icon1shape == icon2shape and icon1color==icon2color:
                    winsound.Beep(880,400)
                elif hasWon(revealedBoxes): # check if all pairs found
                    gameWonAnimation(mainboard)
                    pygame.time.wait(2000)

                    # reset the board
                    mainboard = getRandomizedBoard()
                    revealedBoxes = generateRevealedBoxesData(False)
                    # show the fully unrevealed board for a second
                    drawBoard(mainboard, revealedBoxes)
                    pygame.display.update()
                    pygame.time.wait(1000)
                    # replay the start game animation
                    startGameAnimation(mainboard)

                # reset first selection variable
                # after second box clicked
                firstselection = None 
            #---------> end of second box clicked ----------------------------------------------------------

        # redraw the screen and wait a clock tick
        pygame.display.update()
        fpsclock.tick(fps)
        #-------------- end of 'mouse is over a box' -----------------------------------------------------------

######## help functions ##############
def generateRevealedBoxesData(val):
    # [  <--- board Width ----> 
    #  [False,False,False,......],
    #  [False,False,False,......],
    #  [False,False,False,......],
    #   .......................
    #  ]
    revealedBoxes = list()
    for i in range(boardwidth):
        revealedBoxes.append( [val]*boardheight )
    return revealedBoxes

def getRandomizedBoard():
    # get a list of every possible shape in every possible color
    # from itertools import product
    # icons = list( product(allshapes,allcolors) ) 
    icons = list()
    for color in allcolors:
        for shape in allshapes:
            icons.append((shape,color))
    # randomize the order of the icons list
    random.shuffle(icons)
    # calculate how many icons are needed
    numiconsused = int( boardwidth*boardheight/2 )
    # need pairs
    icons = icons[:numiconsused] * 2 # [1,2,3]*2 = [1,2,3,1,2,3]
    random.shuffle(icons)

    # create the board data structure, with randomly placed icons
    board = list()
    for x in range(boardwidth):
        column = []
        for y in range(boardheight):
            column.append( icons.pop() )
        board.append(column)
    return board

def splitIntoGroupsOf(groupsize,thelist):
    # splits a list into a list of lists, where inner lists have at
    # most groupsize number of items
    results = []
    for i in range(0, len(thelist),groupsize):
        results.append(thelist[i : i+groupsize])
    return results

def leftTopCoordsOfBox(box):
    # convert board coordinates to pixel coordinates
    left = box.x * (boxsize + gapsize) + xmargin
    top  = box.y * (boxsize + gapsize) + ymargin
    return left,top

def getBoxAtPixel(x,y):
    " Converting from Pixel Coordinates to Box Coordinates "
    # Rect objects have a collidepoint() method that you can pass X and Y coordinates too, and
    # it will return True if the coordinates are inside (that is, collide with) the Rect object's area
    for boxX in range(boardwidth):
        for boxY in range(boardheight):
            left,top = leftTopCoordsOfBox( Box(boxX,boxY) )
            boxrect = pygame.Rect(left,top,boxsize,boxsize)
            if boxrect.collidepoint(x,y):
                return Box(boxX,boxY)
    return Box(None,None)

def drawIcon(shape,color,box):
    quarter = int(boxsize/4)
    half    = int(boxsize/2)
    left,top = leftTopCoordsOfBox(box)
    # draw the shapes
    if shape == donut:
        pygame.draw.circle(surface,color,(left+half,top+half),half-5)
        pygame.draw.circle(surface,bgcolor,(left+half,top+half),quarter-5)
    elif shape == square:
        pygame.draw.rect(surface,color,(left+quarter,top+quarter,boxsize-half,boxsize-half) )
    elif shape == diamond:
        pygame.draw.polygon(surface,color,((left+half,top), (left+boxsize-1,top+half),(left+half,top+boxsize-1),(left,top+half) ) )
    elif shape == lines:
        for i in range(0,boxsize,4):
            pygame.draw.line(surface,color,(left,top+i),(left+i,top))
            pygame.draw.line(surface,color,(left+i,top+boxsize-1),(left+boxsize-1,top+i))
    elif shape == oval:
        pygame.draw.ellipse(surface,color, (left, top+quarter,boxsize,half) )
def getShapeAndColor(board,box):
    # shape value for x,y spot is stored in board[x][y][0]
    # color value for x,y spot is stored in board[x][y][1]
    return board[box.x][box.y][0], board[box.x][box.y][1]

def drawBoxCovers(board,boxes,coverage):
    # draw boxes being covered/revealed.
    #'boxes' is a list of  tuples (X,Y)
    # boxes = [(boxX1,boxY2),(boxX2,boxY2),...]
    for boxXY in boxes:
        box = Box(boxXY)
        left,top = leftTopCoordsOfBox(box)
        pygame.draw.rect(surface,bgcolor,(left,top,boxsize,boxsize) )
        shape,color = getShapeAndColor(board, box)
        drawIcon(shape,color,box)
        if coverage > 0: # only draw the cover if there is an coverage
            pygame.draw.rect(surface,boxcolor,(left,top,coverage,boxsize) )
    pygame.display.update()
#   print 'draw Box Covers...'
    fpsclock.tick(fps)

def revealBoxesAnimation(board,boxesToReveal):
    # do the 'box reveal' animation
    for coverage in range(boxsize,(-revealspeed)-1,-revealspeed):
        drawBoxCovers(board,boxesToReveal,coverage)

def coverBoxesAnimation(board,boxesToCover):
    # do the 'box cover' animation
    for coverage in range(0, boxsize+revealspeed, revealspeed):
        drawBoxCovers(board,boxesToCover,coverage)

def drawBoard(board,revealed):
    # draws all of the boxes in their covered or revealed state
    for boxX in range(boardwidth):
        for boxY in range(boardheight):
            box = Box(boxX,boxY)
            left,top = leftTopCoordsOfBox(box)
            if not revealed[boxX][boxY]:
                # draw a covered box
                pygame.draw.rect(surface,boxcolor,(left,top,boxsize,boxsize))
            else:
                # draw the (revealed) icon
                shape,color = getShapeAndColor(board,box)
                drawIcon(shape,color,box)
def drawHightlightBox(box):
    left,top = leftTopCoordsOfBox(box)
    pygame.draw.rect(surface,highlightcolor,(left-5,top-5,boxsize+10,boxsize+10),4)

def startGameAnimation(board):
    # randomly reveal the boxes 8 at a time
    coveredboxes = generateRevealedBoxesData(False)
    boxes = list( product(range(boardwidth),range(boardheight)) )
    random.shuffle(boxes)
    boxgroups = splitIntoGroupsOf(8,boxes)

    drawBoard(board,coveredboxes)

    for boxgroup in boxgroups:
        revealBoxesAnimation(board,boxgroup)
        coverBoxesAnimation(board,boxgroup)

def gameWonAnimation(board):
    # flash the background color when the player has won
    coveredboxes = generateRevealedBoxesData(True)
    color1 = lightbgcolor
    color2 = bgcolor

    for i in range(13):
        # swap colors
        color1,color2 = color2, color1
        surface.fill(color1)
        drawBoard(board,coveredboxes)
        pygame.display.update()
        pygame.time.wait(300)

def hasWon(revealedBoxes):
    # returns True if all the boxes has been revealed, otherwise False
    for i in revealedBoxes:
        if False in i:
            # return False if any of boxes are covered
            return False
    return True

if __name__ == '__main__':
    main()




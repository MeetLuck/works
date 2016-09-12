import pygame, sys, random, winsound
from pygame.locals import *
from itertools import product

fps = 80
resolution = 640,480
width,height = resolution
# speed boxes' sliding reveals and covers
revealspeed = 8
# size of box height & width
boxsize = 40
# size of gap between boxes
gapsize = 10
# number of columns and heights of icons 
boardwidth,boardheight = 8,5
assert (boardwidth * boardheight) % 2 == 0, 'board need to have an even number of boxes for pairs of matches'
xmargin = int( (width  - boardwidth*(boxsize+gapsize))/2 )
ymargin = int( (height - boardheight*(boxsize+gapsize))/2 )

#            R    G    B
gray     = (100, 100, 100)
navyblue = ( 60,  60, 100)
white    = (255, 255, 255)
red      = (255,   0,   0)
green    = (  0, 255,   0)
blue     = (  0,   0, 255)
yellow   = (255, 255,   0)
orange   = (255, 128,   0)
purple   = (255,   0, 255)
cyan     = (  0, 255, 255)


bgcolor = navyblue
lightbgcolor = gray
boxcolor = white
highlightcolor = blue

donut = 'donut'
square = 'square'
diamond = 'diamond'
lines = 'lines'
oval = 'oval'

allcolors = red,green,blue,yellow #,orange,purple,cyan
allshapes = donut,square,diamond,lines,oval
assert len(allcolors)*len(allshapes)*2 >= boardwidth*boardheight, 'Board is too big for the number of shapes/colored defined'

def main():
    global fpsclock, surface
    pygame.init()
    fpsclock = pygame.time.Clock()
    surface = pygame.display.set_mode(resolution)
    # store x,y coordinate of mouse event
    mousex,mousey = 0,0 
    pygame.display.set_caption('Memory Game')

    mainboard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    # store (x,y) of the first box clicked
    firstselection = None 
    surface.fill(bgcolor)
    startGameAnimation(mainboard)


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

        boxx,boxy = getBoxAtPixel(mousex,mousey)
        if boxx != None and boxy != None: # check if the mouse is currently over a box.
            # the mouse is currently over a box
            if not revealedBoxes[boxx][boxy]:
                drawHightlightBox(boxx,boxy)

            if not revealedBoxes[boxx][boxy] and mouseclicked:
                winsound.Beep(500,50)
                revealBoxesAnimation(mainboard, [(boxx,boxy)])
                # set the box as revealed
                # whether icon1 == icon2 or not
                # whether first selection or second selection
                revealedBoxes[boxx][boxy] = True

                # the current box was first box clicked
                if firstselection == None:
                    firstselection = boxx,boxy
                # the current box was the second box clicked
                # check if there is a match between the two icons
                else:
                # ---> second box clicked ------------------------------------------------------------------
                    icon1shape,icon1color = getShapeAndColor(mainboard,firstselection[0],firstselection[1])
                    icon2shape,icon2color = getShapeAndColor(mainboard,boxx,boxy)

                    if icon1shape != icon2shape or icon1color != icon2color:
                        # icons don't match. Re-cover up both selections
                        # set reaveledBoxes(first selction) = False
                        # set reaveledBoxes(second selction) = False
                        pygame.time.wait(200) # 1000 msec = 1 sec
                        coverBoxesAnimation(mainboard, [(firstselection[0],firstselection[1]),(boxx,boxy)])
                        revealedBoxes[firstselection[0]][firstselection[1]] = False
                        revealedBoxes[boxx][boxy] = False
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
                #---------> end of second box clicked ---------------------------------------------------

            # redraw the screen and wait a clock tick
            pygame.display.update()
            fpsclock.tick(fps)

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

def leftTopCoordsOfBox(boxx,boxy):
    # convert board coordinates to pixel coordinates
    left = boxx*(boxsize + gapsize) + xmargin
    top  = boxy*(boxsize + gapsize) + ymargin
    return left,top

def getBoxAtPixel(x,y):
    " Converting from Pixel Coordinates to Box Coordinates "
    # Rect objects have a collidepoint() method that you can pass X and Y coordinates too, and
    # it will return True if the coordinates are inside (that is, collide with) the Rect object's area
    for boxx in range(boardwidth):
        for boxy in range(boardheight):
            left,top = leftTopCoordsOfBox(boxx,boxy)
            boxrect = pygame.Rect(left,top,boxsize,boxsize)
            if boxrect.collidepoint(x,y):
                return boxx,boxy
    return None,None

def drawIcon(shape,color,boxx,boxy):
    quarter = int(boxsize/4)
    half    = int(boxsize/2)
    left,top = leftTopCoordsOfBox(boxx,boxy)
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
def getShapeAndColor(board,boxx,boxy):
    # shape value for x,y spot is stored in board[x][y][0]
    # color value for x,y spot is stored in board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawBoxCovers(board,boxes,coverage):
    # draw boxes being covered/revealed.
    #'boxes' is a list of  tuples (X,Y)
    # boxes = [(boxX1,boxY2),(boxX2,boxY2),...]
    for box in boxes:
        left,top = leftTopCoordsOfBox(box[0],box[1])
        pygame.draw.rect(surface,bgcolor,(left,top,boxsize,boxsize) )
        shape,color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape,color,box[0],box[1])
        if coverage > 0: # only draw the cover if there is an coverage
            pygame.draw.rect(surface,boxcolor,(left,top,coverage,boxsize) )
    pygame.display.update()
    print 'draw Box Covers...'
    fpsclock.tick(fps/10)

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
    for boxx in range(boardwidth):
        for boxy in range(boardheight):
            left,top = leftTopCoordsOfBox(boxx,boxy)
            if not revealed[boxx][boxy]:
                # draw a covered box
                pygame.draw.rect(surface,boxcolor,(left,top,boxsize,boxsize))
            else:
                # draw the (revealed) icon
                shape,color = getShapeAndColor(board,boxx,boxy)
                drawIcon(shape,color,boxx,boxy)
def drawHightlightBox(boxx,boxy):
    left,top = leftTopCoordsOfBox(boxx,boxy)
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




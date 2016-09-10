import pygame, sys, random
from pygame.locals import *
fps = 30
resolution = 640,480
width,height = resolution
# speed boxes' sliding reveals and covers
revealspeed = 8
# size of box height & width
boxsize = 40
# size of gap between boxes
gapsize = 10
# number of columns and heights of icons 
boardwitdth,boardheight = 10,7
assert (boardwidth * boardheight) % 2 == 0, 'board need to have an even number of boxes for pairs of matches'
xmargin = int( (width-boardwidth*(boxsize+gapsize))/2 )
ymargin = int( (height-boardheight*(boxsize+gapsize))/2 )

# R G B
colors = pygame.color.THECOLORS
gray = colors['gray']
navyblue = colors['navyblue']
white = colors['white']
red = colors['red']
green = colors['green']
blue = colors['blue']
yellow = colors['yellow']
orange = colors['orange']
purple = colors['purple']
cyan = colors['cyan']

bgcolor = navyblue
lightbgcolor = gray
boxcolor = white
highlightcolor = blue

donut = 'donut'
square = 'square'
diamond = 'diamond'
lines = 'lines'
oval = 'oval'

allcolors = red,green,blue,yellow,orange,purple,cyan
allshapes = donut,square,diamond,lines,oval
assert len(allcolors)*len(allshapes)*2 >= boardwidth*boardheight, 'Board is too big for the number of shapes/colored defined'

def main():
    global fpsclock, surface
    pygame.init()
    fpsclock = pygame.time.Clock()
    surface = pygame.display.set_mode(resolution)
    mousex,mousey = 0,0 # used to store x,y coordinate of mouse event
    pygame.display.set_caption('Memory Game')

    mainboard = getrandomizeboard()
    revealedboxes = generaterevealedboxesdata(False)

    # store (x,y) of the first box clicked
    firstselection = None 
    surface.fill(bgcolor)
    startgameanimation(mainboard)

    while True: # main loop
        mouseclicked = False
        surface.fill(bgcolor)
        drawboard(mainboard, revealedboxes)

        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                pygame.quit(); sys.exit()
            elif e.type == MOUSEMOTION:
                mousex,mousey = e.pos
            elif e.type == MOUSEBUTTONUP:
                mousex,mousey = e.pos
                mouseclicked = True
        boxx,boxy = getboxatpixel(mousex,mousey)
        if boxx != None and boxy != None:
            # the mouse is currently over a box
            if not revealedboxes[boxx][boxy]:
                drawhighlightbox(boxx,boxy)
            if not revealedboxes[boxx][boxy] and mouseclicked:
                revealboxesanimation(mainboard, [(boxx,boxy)])
                revealedboxes[boxx][boxy] = True # set the box as revealed
                if firstselection == None: # the current box was the first box clicked
                    firstselection = boxx,boxy
                else: # the current box was the second box clicked
                    # check if there is a match between the two icons
                    icon1shape,icon1color = getshapeandcolor(mainboard,firstselection[0],firstselection[1])
                    icon2shape,icon2color = getshapeandcolor(mainboard,boxx,boxy)

                    if icon1shape != icon2shape or icon1color != icon2color:
                        # icons don't match. Re-cover up both selections
                        pygame.time.wait(1000) # 1000 msec = 1 sec
                        coverboxesanimation(mainboard, [(firstselection[0],firstselection[1]),(boxx,boxy)])
                        revealedboxes[firstselection[0]][firstselection[1]] = False
                        revealedboxes[boxx][boxy] = False
                    elif haswon(revealedboxes): # check if all pairs found
                        gamewonanimation(mainboard)
                        pygame.time.wait(2000)

                        # reset the board
                        mainboard = getrandomizedboard()
                        revealedboxes = generaterevealedboxesdata(False)
                        # show the fully unrevealed board for a second
                        drawboard(mainboard, revealedboxes)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        # replay the start game animation
                        startgameanimation(mainboard)

                    # reset first selection variable
                    firstselection = None 

                # redraw the screen and wait a clock tick
                pygame.display.update()
                fpsclock.tick(fps)

######## help functions ##############
def generaterevealedboxesdata(val):
    revealedboxes = list()
    for i in range(boardwidth):
        revealedboxes.append( [val]*boardheight )
    return revaledboxes

def getrandomizedboard():
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
    icons = icons[:numiconsused] * 2
    random.shuffle(icons)

    # create the board data structurem, with randomly placed icons
    board = list()
    for x in range(boardwidth):
        column = list()
        for y in range(boardheight):
            column.append(icons[0])
            # remove the icons as we assign them
            del icons[0]
        board.append(column)
    return board
def splitintogroupsof(groupsize,thelist):
    # splits a list into a list of lists, where inner lists have at
    # most groupsize number of items
    results = []
    for i in range(0, len(thelist),groupsize):
        result.append(thelist[i : i+groupsize])
    return result

def lefttopcoordsofbox(boxx,boxy):
    # convert board coordinates to pixel coordinates
    left = boxx*(boxsize + gapsize) + xmargin
    top  = boxx*(boxsize + gapsize) + ymargin
    return left,top
def getboxatpixel(x,y):
    for boxx in range(boardwidth):
        for boxy in range(boardheight):
            left,top = lefttopcoordsofbox(boxx,boxy)
            boxrect = pygame.Rect(left,top,boxsize,boxsize)
            if boxrect.collidepoint(x,y):
                return boxx,boxy
    return None,None
def drawicon(shape,color,boxx,boxy):
    quarter = int(boxsize/4)
    half    = int(boxsize/2)
    left,top = lefttopcoordsofbox(boxx,boxy)
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
    elif shape =- oval:
        pygame.draw.ellips(surface,color, (left, top+quarter,boxsize,half) )
def getshapeandcolor(board,boxx,boxy):
    # shape value for x,y spot is stored in board[x][y][0]
    # color value for x,y spot is stored in board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawboxcovers(board,boxes,coverage):
    # draw boxes being covered/revealed. 'boxes' is a list
    # of tow-item lists, which have x & y spot of the box
    for box in boxes:
        left,top = lefttopcoordsofbox(box[0],box[1])
        pygame.draw.rect(surface,bgcolor,(left,top,boxsize,boxsize) )
        shape,color = getshapeandcolor(board, box[0], box[1])
        drawicon(shape,color,box[0],box[1])
        if coverage > 0: # only draw the cover if there is an coverage
            pygame.draw.rect(surface,boxcolor,(left,top,coverage,boxsize) )
        pygame.display.update()
        fpsclock.tick(fps)
def revealboxesanimation(board,boxestoreveal):
    # do the 'box reveal' animation
    for coverage in range(boxsize,(-revealspeed)-1,-revealspeed):
        drawboxcovers(board,boxestoreveal,coverage)




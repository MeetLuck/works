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



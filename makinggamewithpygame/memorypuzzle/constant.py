'''     Boxs coordinates

  +---------------- boxX ----------->
  | 
  |   +----+ +----+ +----+ +----+
  |   |    | |    | |    | |    |
  |   +----+ +----+ +----+ +----+
  |   +----+ +----+ +----+ +----+
  |   |    | |    | |    | |    |
  |   +----+ +----+ +----+ +----+
  |   +----+ +----+ +----+ +----+
  |   |    | |    | |    | |    |
  |   +----+ +----+ +----+ +----+
  |
  v
  boxY 

'''
fps = 40
resolution = 640,480 ; width,height = resolution
# speed of boxes' sliding reveals and covers
revealspeed = 8 #8
# size of box height & width
boxsize = 60
# size of gap between boxes
gapsize = 10

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

# number of columns and heights of icons(boxes) 
#boardwidth,boardheight = 6,5
boardwidth,boardheight = 5,4
assert (boardwidth * boardheight) % 2 == 0, 'board need to have an even number of boxes for pairs of matches'
xmargin = int( (width  - boardwidth*(boxsize+gapsize))/2 )
ymargin = int( (height - boardheight*(boxsize+gapsize))/2 )

allcolors = red,green,blue,yellow #,orange,purple,cyan
allshapes = donut,square,diamond,lines,oval
assert len(allcolors)*len(allshapes)*2 >= boardwidth*boardheight, 'Board is too big for the number of shapes/colored defined'


#class Box:
#    def __init__(self,x):
#        self.x = x
#        self.y = y

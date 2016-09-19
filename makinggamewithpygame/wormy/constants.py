# warm constants
# warm = [head,body]     tbbbbbbh -> right
# del t, insert new head  tbbbbbbh -> right
#
# move right     ------->
# remove tail     ------>
# add new head    ------->

fps = 40/8 
width = 640
height = 480
resolution = width,height
cellsize = 20
assert width % cellsize == 0, "Window width must be a multiple of cell size."
assert height % cellsize == 0, "Window height must be a multiple of cell size."
boardwidth = int(width / cellsize)
boardheight = int(height / cellsize)

#             R    G    B
white     = (255, 255, 255)
black     = (  0,   0,   0)
red       = (255,   0,   0)
green     = (  0, 255,   0)
darkgreen = (  0, 155,   0)
darkgray  = ( 40,  40,  40)
bgcolor = black

up = 'up'
down = 'down'
left = 'left'
right = 'right'

head = 0 # syntactic sugar: index of the worm's head

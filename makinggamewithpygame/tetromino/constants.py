fps = 25*2
width,height = 640,480
boxsize = 20
boardwidth,boardheight= 10,20
blank = '.'

up,down,left,right = 'up','down','left','right'

movesidwaysfreq = 0.15
movedownfreq = 0.1

xmargin = (width - boardwidth * boxsize) /2
topmargin = height - boardheight * boxsize - 5

#  R G B
white = 255,255,255
gray = 185,185,185
black = 0,0,0
red = 155,0,0
lightred = 175,20,20
green = 0, 155, 0
lightgreen = 20, 175, 20
blue = 0,0,155
lightblue = 20,20,175
yellow = 155,155,0
lightyellow = 175,175,20


bordercolor = blue
bgcolor = black
boardbgcolor = 40,40,40 
textcolor = white
textshadowcolor = gray
colors = blue, green, red, yellow
lightcolors = lightblue, lightgreen, lightred, lightyellow

templatewidth,templateheight = 5,5

s_shape_template = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

z_shape_template = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

i_shape_template = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

o_shape_template = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

j_shape_template = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

l_shape_template = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

t_shape_template = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]
pieces = { 'S': s_shape_template,
          'Z': z_shape_template,
          'J': j_shape_template,
          'L': l_shape_template,
          'I': o_shape_template,
          'O': t_shape_template }

S = [
list( 
  '.....'+
  '.....'+
  '..##.'+
  '.##..'+
  '.....' ),      
list(
'.....'+
'.#...'+
'.##..'+
'..#..'+
'.....' )
   ]


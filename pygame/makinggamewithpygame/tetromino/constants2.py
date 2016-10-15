from pygame.color import THECOLORS as thecolors
fps = 25 
#width,height = 640,480
width,height = 800,600
boxsize = 25 
boardwidth,boardheight= 10,20
blank = '.'

up,down,left,right = 'up','down','left','right'

movesidwaysfreq = 0.15
movedownfreq = 0.1

xmargin = (width - boardwidth * boxsize) /2
topmargin = height - boardheight * boxsize - 5

#  R G B
white = thecolors['white']
gray = thecolors['gray']
black = thecolors['black']
red = thecolors['red']
blue = thecolors['blue']
skyblue = thecolors['skyblue']
steelblue = thecolors['steelblue']
royalblue = thecolors['royalblue']
green = thecolors['green']
yellow = thecolors['yellow']
purple = thecolors['purple']
orange = thecolors['darkorange']
#lightorange = thecolors['lightorange']
cyan = thecolors['darkcyan']
pink = thecolors['pink']
tan= thecolors['tan']
khaki= thecolors['khaki']
yellowgreen= thecolors['yellowgreen']
#purple = 255,255,255 #gray = 185,185,185 #black = 0,0,0
#red = 155,0,0 #green = 0, 155, 0 #blue = 0,0,155
#yellow = 155,155,0 #purple = 160,32,240 #pink   = 255,192,203
#cyan   = 0,255,255 #orange = 255,165,0


lightgreen = 20, 175, 20
lightred = 175,20,20
lightblue = 20,20,175
lightyellow = 175,175,20


bordercolor = 100,100,100 #blue #20,20,20 #blue
bordercolor2 = 20,20,20 #blue
bgcolor = black
boardbgcolor = bgcolor #20,20,20 
#gridcolor = boardbgcolor[0]+20,boardbgcolor[1]+20, boardbgcolor[2]+ 20
#gridcolor2 = boardbgcolor[0]+30,boardbgcolor[1]+30, boardbgcolor[2]+30
gridcolor = boardbgcolor[0]+40,boardbgcolor[1]+40, boardbgcolor[2]+ 40
gridcolor2 = boardbgcolor[0]+50,boardbgcolor[1]+50, boardbgcolor[2]+50
textcolor = white
textshadowcolor = gray
colors = red,orange,pink,yellow, green, purple, blue, cyan, khaki, tan, yellowgreen,royalblue,skyblue,steelblue
lightcolors = lightblue, lightgreen, lightred, lightyellow

templatewidth,templateheight = 5,5

s_shape_template = [ '.....'+
                     '.....'+
                     '..OO.'+
                     '.OO..'+
                     '.....',
                     '.....'+
                     '..O..'+
                     '..OO.'+
                     '...O.'+
                     '.....' ]

z_shape_template = [ '.....'+
                     '.....'+
                     '.OO..'+
                     '..OO.'+
                     '.....' ,
                     '.....'+
                     '..O..'+
                     '.OO..'+
                     '.O...'+
                     '.....' ]

i_shape_template = [ '..O..'+
                     '..O..'+
                     '..O..'+
                     '..O..'+
                     '.....' ,
                     '.....'+
                     '.....'+
                     'OOOO.'+
                     '.....'+
                     '.....' ]

o_shape_template = [ '.....'+
                     '.....'+
                     '.OO..'+
                     '.OO..'+
                     '.....' ]

j_shape_template = [ '.....'+
                     '.O...'+
                     '.OOO.'+
                     '.....'+
                     '.....' ,
                     '.....'+
                     '..OO.'+
                     '..O..'+
                     '..O..'+
                     '.....' ,
                     '.....'+
                     '.....'+
                     '.OOO.'+
                     '...O.'+
                     '.....' ,
                     '.....'+
                     '..O..'+
                     '..O..'+
                     '.OO..'+
                     '.....' ]

l_shape_template = [ '.....'+
                     '...O.'+
                     '.OOO.'+
                     '.....'+
                     '.....',
                     '.....'+
                     '..O..'+
                     '..O..'+
                     '..OO.'+
                     '.....' ,
                     '.....'+
                     '.....'+
                     '.OOO.'+
                     '.O...'+
                     '.....' ,
                     '.....'+
                     '.OO..'+
                     '..O..'+
                     '..O..'+
                     '.....' ]

t_shape_template = [ '.....'+
                     '..O..'+
                     '.OOO.'+
                     '.....'+
                     '.....' ,
                     '.....'+
                     '..O..'+
                     '..OO.'+
                     '..O..'+
                     '.....' ,
                     '.....'+
                     '.....'+
                     '.OOO.'+
                     '..O..'+
                     '.....' ,
                     '.....'+
                     '..O..'+
                     '.OO..'+
                     '..O..'+
                     '.....']
pieces = { 'S': s_shape_template,
          'Z': z_shape_template,
          'J': j_shape_template,
          'L': l_shape_template,
          'I': i_shape_template,
          'O': o_shape_template,
          'T': t_shape_template }

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


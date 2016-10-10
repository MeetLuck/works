import pygame,random,os

# colors
white = pygame.Color('white')
red = pygame.Color('red')
blue = pygame.Color('blue')
black = pygame.Color('black')
yellow = pygame.Color('yellow')
color02 = (66,1,166)
color1 = red
color2 = (0,255,155)
color3 = (100,55,155)
color4 = (250,100,255)
color5 = color4

# check for Quit event
def checkQuit(): # event handler
    for e in pygame.event.get():
        if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            return False
        pygame.event.post(e)
    return True

#### configuration
mapcolors =\
{ 'x': (100,60,30),
  'y': (30,120,10),
  'u': (30,190,10),
  'r': (250,250,0),
  'e': (250,0,0) }
config =\
{ 'fullscreen': False,
  'visibmouse': False,
  'width': False,
  'height': False,
  'bgcolor': False,
  'fontratio': False,
  'fontcolor': False,
  'fps': False,
  'friction': False,
  'playersizefac': False,
  'playeraccel': False,
  'widthsensors': False,
  'heightsensors': False,
  'title': "Maze Wanderer",
  'waitingtext': 'quit=ESC, again=Other Key'
  }

### maps
# x = wall
# s = start
# d = level down
# u = level up
# r = random level

# 20 x 16
easy_map =\
["xxxxxxxxxxxxxxxxxxxx",
 "xs.....x...........x",
 "xxxx.......xxxx....x",
 "x.rx.......x..x..xxx",
 "x..x...x......x...dx",
 "x......x......x....x",
 "x...xxxx..xx.......x",
 "x...x.....x........x",
 "x.............x..xxx",
 "xxxxxx.x...xxxx...rx",
 "x......x......x....x",
 "x......x...........x",
 "xxx..x.....xx......x",
 "xrx..xxxx..x...xxxxx",
 "x.................ux",
 "xxxxxxxxxxxxxxxxxxxx"]

# 22 x 16
medium_map =\
["xxxxxxxxxxxxxxxxxxxxxx",
 "xs................x.rx",
 "xxx...x......x....x..x",
 "x.....xx.xxxxxxx.....x",
 "x..x..x..xr...x.....xx",
 "x..xxxx..xx..........x",
 "x.....x..x..xx..xx...x",
 "xxxx.............x.d.x",
 "x......xxx....x..xxx.x",
 "x...x..x....xxxd.....x",
 "xd..x..x..x.......x..x",
 "x...x.xx..xxxxx...x..x",
 "x..xx.........x...x.xx",
 "xx......xx...........x",
 "xr.......x.........xux",
 "xxxxxxxxxxxxxxxxxxxxxx"]

# 26 x 19
hard_map =\
["xxxxxxxxxxxxxxxxxxxxxxxxxx",
 "xs....x........x.....x..rx",
 "xxxx..xx..xxx..x..x..x..xx",
 "x..........x......x......x",
 "x..xxx.....x..xxxxx...xxxx",
 "x..x.....................x",
 "x..x.xxxxxx.x..x.....xx..x",
 "x....xr.....x..xxxx..xd..x",
 "xxx..x......x..xd....xxxxx",
 "x....xxxxx.xx..x..x......x",
 "x........x........x...x.xx",
 "x............x..xxxx..x..x",
 "xx...xxxxx.........x..x..x",
 "x.....x......xxxx........x",
 "x..xxxx...xxxx.rx...x....x",
 "x............x..x...x....x",
 "xxxxxxx..x...x..x..xx..xxx",
 "xd.......x...x..........ex",
 "xxxxxxxxxxxxxxxxxxxxxxxxxx"]

# 5 x 8
test_map=\
["xxxxx",
 "xs..x",
 "x..ux",
 "x..dx",
 "x..rx",
 "x..ex",
 "x...x",
 "xxxxx"]

# game maps
maps =  easy_map, medium_map, hard_map

# testing
# maps = test_map, easy_map, medium_map, hard_map

#### map constants

UP = 1
DOWN = -1
RANDOM = -2
START = -3
PLACES = set(('u', 'd', 'r', 'e'))
NOT_DRAWABLES = set(('.', 's'))


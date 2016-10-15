'''
007 loading files from folders and subsurfaces.py
press p to toggle painting of pretty background
press d to toggle dirty rect painting
press r to restore the ugly image
'''
from constants import *

pygame.init()
screen = pygame.display.set_mode( (800,470) )
screenrect = screen.get_rect()

folder = 'data'
try: # try to load images from the harddisk
    prettysurf = pygame.image.load(os.path.join(folder, "800px-La_naissance_de_Venus.jpg"))
    uglysurf = pygame.image.load(os.path.join(folder, "background800x470.jpg"))
    snakesurf = pygame.image.load(os.path.join(folder,"snake.gif")) # with tranparent colour
except:
     msg= "\nSadly i could not open one of those pictures from the folder 'data': \n"
     msg+="800px-La_naissance_de_Venus.jpg \n"
     msg+="background800x470.jpg \n"
     msg+="snake.gif \n"
     msg+="please make sure that files and folder exist. \n"
     msg+="see http://thepythongamebook.com/en:part2:pygame:step007 for more information"
     raise( UserWarning, msg ) # print error message and exit program 

prettysurf = prettysurf.convert()
uglysurf = uglysurf.convert()
bgsurf = uglysurf.copy() # actual background
snakesurf = snakesurf.convert_alpha()
snakerect = snakesurf.get_rect()

# start position for snake surf
x,y = 1,1
dx,dy = 40,85 # speed of ball surf in pixel per second
screen.blit(uglysurf,(0,0))  # blit the background on screen
screen.blit(snakesurf,(x,y)) # blit ball surf on the screen
clock = pygame.time.Clock()
mainloop = True
fps = 60
playtime = 0
painting = False # do not overpaint the ugly surf yet
dirty = False    # do clear dirty part of screen

while mainloop:
    milisecconds = clock.tick(fps)
    seconds   = milisecconds/1000.0
    playtime += seconds
    mainloop = checkQuit()
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r:
                bgsurf = uglysurf.copy()
                screen.blit(uglysurf,(0,0))
                print 'pressed r,  ugly background restored'
            elif e.key == pygame.K_p:
                painting = not painting  # toggle painting
                print 'pressed p,  painting is now set to {}'.format(painting)
            elif e.key == pygame.K_d:
                dirty = not dirty
                print 'pressed d, dirty is now set to {}'.format(dirtyrect)

    pygame.display.set_caption( "FPS: {:.2f} dx:{} dy:{} [p]aint ({}) paint, [d]irtyrect ({}), [r]estore".
                               format(clock.get_fps(), dx, dy, painting, dirty)  )
    # this would repaint the whole screen, secure but slow
    # screen.blit(bgsurf,(0,0)) # draw background on screen (overwriting all)
    # this only repaints the dirty part of the screen
    if not dirty: # calculate dirtyrect and blit it
        #print x,y, snakerect
        dirtyrect = bgsurf.subsurface( (x,y,snakerect.width, snakerect.height) )
        screen.blit( dirtyrect, (x,y) )
    x += seconds * dx
    y += seconds * dy
    # bounce snake if out of screen
    if x < 0:
        x = 0
        dx *= -1
        dx += random.randint(-15,15) # new random direction
    elif x + snakerect.width >= screenrect.width:
        ballx = screenrect.width - snakerect.width
        dx *= -1
        dx += random.randint(-15,15)
    if y < 0 :
        y = 0
        dy *= -1
        dy += random.randint(-15,15)
    elif y + snakerect.height >= screenrect.height:
        y = screenrect.height - snakerect.height
        dy *= -1
        dy += random.randint(-15,15)
    # paint the snake
    screen.blit(snakesurf,(x,y))
    # TV corner: paint a subsurface on the screen of this part of pretty background
    # where snake is at the moment (rect argument)
    try:
        tvscreen = prettysurf.subsurface( (x,y,snakerect.width, snakerect.height) )
    except:
        print 'subsurface not working'
    screen.blit( tvscreen, (0,0) ) # blit into screen like a tv
    if painting: bgsurf.blit(tvscreen,(x,y))  # blit from pretty background into background
    pygame.display.flip()
print "This 'game' was played for {:.2f} seconds".format(playtime)






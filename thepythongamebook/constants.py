import pygame,random,os
# fps
fps = 50
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

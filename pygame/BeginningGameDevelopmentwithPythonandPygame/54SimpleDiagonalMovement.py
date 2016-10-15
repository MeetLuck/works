# Listing 5-4. Simple Diagonal Movement : move X and Y
import pygame
from pygame.locals import *
from sys import exit

# constants
screensize = screenwidth,screenheight = 640,480
bgimage = 'sushiplate.jpg'
spriteimage = 'fugu.png'
black = pygame.Color('black')
white = pygame.Color('white')
red = pygame.Color('red')
green = pygame.Color('green')
blue = pygame.Color('blue')
 
# initialize pygame 
pygame.init()
screen = pygame.display.set_mode(screensize,0,32)
bgsurf = pygame.image.load(bgimage).convert()
spritesurf = pygame.image.load(spriteimage).convert_alpha()
# clock object
clock = pygame.time.Clock()

def getText(msg,color=blue):
    font = pygame.font.SysFont('bitstreamveraserif',20)
    textsurf = font.render(msg,True,color) # font.render(text,antialias,fg,bg)
    return textsurf

# X coordinate of our sprite
x,y = 0,0
fps = 60
# Speed in pixels per seconds
speedX,speedY = 133,170

while True:
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit(); exit()

    screen.blit(bgsurf,(0,0))
    screen.blit(spritesurf, (x,y) )

    # time passed(milliseconds) = clock.tick()
    timepassed = clock.tick(fps)/1000.0
    dx = round(timepassed * speedX,0)
    dy = round(timepassed * speedY,0)
    x += dx
    y += dy

    # if the sprite goes off the edge of the screen
    # make it move in the opposite direction
    if x > screenwidth - spritesurf.get_width():
        speedX = -speedX
        x = screenwidth - spritesurf.get_width()
    elif x < 0:
        speedX = -speedX
        x = 0
    if y > screenheight - spritesurf.get_height():
        speedY = -speedY
        y = screenheight - spritesurf.get_height()
    elif y < 0:
        speedY = -speedY
        y = 0
    pygame.display.update()


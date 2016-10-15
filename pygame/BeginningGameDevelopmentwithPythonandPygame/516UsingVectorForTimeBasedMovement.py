# Listing 5-4. Simple Diagonal Movement : move X and Y
import pygame
from pygame.locals import *
from sys import exit
from gameobjects.vector2 import Vector2

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
fps = 60
# Speed in pixels per seconds
speed = 250.0
position = Vector2(100,100)
heading = Vector2()

while True:
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit(); exit()
        if event.type == MOUSEBUTTONDOWN:
            destination = Vector2(*event.pos) - Vector2(*spritesurf.get_size())/2.0
            heading = Vector2.from_points(position,destination)
            heading.normalize()

    screen.blit(bgsurf,(0,0))
    screen.blit(spritesurf, position)

    # time passed(milliseconds) = clock.tick()
    timepassed = clock.tick(fps)/1000.0
    distancemoved = timepassed * speed
    position += distancemoved * heading
    pygame.display.update()

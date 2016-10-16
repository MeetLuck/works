# Listing 6-4. Rotational Mouse Movement
import pygame
from pygame.locals import *
from sys import exit
from gameobjects.vector2 import Vector2
from math import *

# constants
screensize = screenwidth,screenheight = 640,480
bgimage = 'sushiplate.jpg'
spriteimage = 'fugu.png'
black = pygame.Color('black')
white = pygame.Color('white')
red = pygame.Color('red')
green = pygame.Color('green')
blue = pygame.Color('blue')
fps = 60
pos = Vector2(200,150)
speed = 300
rotation = 0
rotationspeed = 360  # degrees per second
 
# initialize pygame 
pygame.init()
screen = pygame.display.set_mode(screensize,0,32)
bgsurf = pygame.image.load(bgimage).convert()
spritesurf = pygame.image.load(spriteimage).convert_alpha()
# clock object
clock = pygame.time.Clock()
# mouse
pygame.mouse.set_visible(True)
pygame.event.set_grab(True)

def getText(msg,color=blue,fontsize=18):
    font = pygame.font.SysFont('bitstreamveraserif',fontsize)
    textsurf = font.render(msg,True,color) # font.render(text,antialias,fg,bg)
    return textsurf


while True:
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit(); exit()

    # pressed keys
    pressedkeys = pygame.key.get_pressed()
    pressedmouse = pygame.mouse.get_pressed()
    rotation_direction = 0
    movement_direction = 0

    rotation_direction = pygame.mouse.get_rel()[0]/3.0
    if pressedkeys[K_LEFT]:     rotation_direction = +1.0
    elif pressedkeys[K_RIGHT]:  rotation_direction = -1.0
    elif pressedkeys[K_UP] or pressedmouse[0]:
        movement_direction = +1.0
    elif pressedkeys[K_DOWN] or pressedmouse[2]:
        movement_direction = -1.0

    screen.blit(bgsurf,(0,0))

    rotatedsprite = pygame.transform.rotate(spritesurf, rotation)
    w,h = rotatedsprite.get_size()
    rotatedpos = Vector2(pos.x-w/2, pos.y-h/2)
    screen.blit(rotatedsprite, (rotatedpos.x,rotatedpos.y) )
    timepassed = clock.tick(fps)/1000.0
    rotation += rotation_direction * speed * timepassed
    headingX = sin(rotation * pi/180.0)
    headingY = cos(rotation * pi/180.0)
    heading = Vector2(headingX,headingY)
    heading *= movement_direction
    pos += speed * timepassed * heading
    pygame.display.update()


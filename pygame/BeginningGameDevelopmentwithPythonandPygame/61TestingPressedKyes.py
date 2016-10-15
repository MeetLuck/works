# Listing 6-1. Testing Pressed Keys
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
fps = 60
 
# initialize pygame 
pygame.init()
screen = pygame.display.set_mode(screensize,0,32)
bgsurf = pygame.image.load(bgimage).convert()
spritesurf = pygame.image.load(spriteimage).convert_alpha()
# clock object
clock = pygame.time.Clock()

def getText(msg,color=blue,fontsize=18):
    font = pygame.font.SysFont('bitstreamveraserif',fontsize)
    textsurf = font.render(msg,True,color) # font.render(text,antialias,fg,bg)
    return textsurf


while True:
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit(); exit()
    screen.fill(white)
    # pressed keys
    pressedkeys_text = []
    pressedkeys = pygame.key.get_pressed()
    y = 32 
    for key,pressed in enumerate(pressedkeys):
        if pressed:
            keyname = pygame.key.name(key)
            keysurf = getText(keyname+' pressed', red,32)
            screen.blit(keysurf, (32,y) )
            y += keysurf.get_height()
    pygame.display.update()

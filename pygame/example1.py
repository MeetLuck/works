# import pygame modules
import pygame,time,math,sys
from pygame.locals import *
# basic screen initialisation
screen = pygame.display.set_mode((800,600))
flight = pygame.image.load('flight.png')
k_up=k_down=k_left=k_right = 0
speed = direction = 0
position = 100,100
turn_speed = 5
acceleration = 2
max_forward_speed = 10
max_reverse_speed = -5
black = 0,0,0
while True:
    pygame.time.Clock().tick(30)
    for event in pygame.event.get():
        if not hasattr(event,'key'): continue
        down = event.type == KEYDOWN
        if event.key == K_RIGHT: k_right = -5 * down
        elif event.key==K_LEFT: k_left = 5 * down
        elif event.key==K_UP: k_up = 2 * down
        elif event.key==K_DOWN: k_down = -2 * down
        elif event.key==K_ESCAPE: sys.exit(0)
    screen.fill(black)
    # simulation
    # new speed and directions based on acceleration and turn
    speed += k_up + k_down
    if speed > max_forward_speed: speed = max_forward_speed
    if speed < max_reverse_speed: speed = max_reverse_speed
    direction += k_right + k_left
    # new position based on current position, speed and direction
    x,y = position
    rad = direction * math.pi/180
    x += -speed * math.sin(rad)
    y += -speed * math.cos(rad)
    position = x,y
    # rendering
    # rotate the car image for direction
    rotated = pygame.transform.rotate(flight, direction)
    # position the car on screen
    rect = rotated.get_rect()
    rect.center = position
    # render the car to screen
    screen.blit(rotated, rect)
    pygame.display.flip()


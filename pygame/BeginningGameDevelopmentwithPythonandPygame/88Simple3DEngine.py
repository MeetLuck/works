# Listing 8-8 Simple 3D Engine(simple3d.py)
import pygame
from pygame.locals import *
from gameobjects.vector3 import Vector3
from math import *
from random import randint

# constants
screensize = screenwidth,screenheight = 640,480
cubesize = 300
black = pygame.Color('black')
white = pygame.Color('white')
fps = 60

def calculateViewingDistance(fov, screenwidth):
    d = screenwidth/2.0 / tan(fov/2.0)
    return d

def main():
    pygame.init()
    screen = pygame.display.set_mode(screensize,0,32)
    defaultfont = pygame.font.get_default_font()
    sysfont = pygame.font.SysFont(defaultfont,24)
    ballsurf = pygame.image.load('ball.png').convert_alpha()

    # the 3D points
    points = []

    fov = 90  # Field of view
    viewdistance = calculateViewingDistance(radians(fov), screenwidth)
    # create a list of points along the edge of a cube
    for x in range(0, cubesize+1, 20):
        isEdgeX  =  (x==0) or (x==cubesize)
        for y in range(0,cubesize+1,20):
            isEdgeY  =  (y==0) or (y==cubesize)
            for z in range(0,cubesize+1,20):
                isEdgeZ  =  (z==0) or (z==cubesize)
                if sum( [isEdgeX, isEdgeY, isEdgeZ] ) >= 2:
                    pointX = x - cubesize/2.0
                    pointY = y - cubesize/2.0
                    pointZ = z - cubesize/2.0
                    points.append( Vector3(pointX,pointY,pointZ) )
    # sort points in z order
    def getPointZ(point):
        return point.z
    points.sort(key=getPointZ, reverse=True)

    centerX,centerY = screenwidth/2, screenheight/2
    ballwidth,ballheight = ballsurf.get_size()
    ballcenterX,ballcenterY = ballwidth/2, ballheight/2
    cameraposition = Vector3(0.0, 0.0, -700.0)
    cameraspeed = Vector3(300.0, 300.0, 300.0)

    clock = pygame.time.Clock()

    while True:
        for e in pygame.event.get():
            if e.type == QUIT: pygame.quit(); exit()
        screen.fill(black)
        pressedkeys = pygame.key.get_pressed()
        timepassed = clock.tick(fps)/1000.0

        direction = Vector3()
        if pressedkeys[K_LEFT]:        direction.x = -1.0
        elif pressedkeys[K_RIGHT]:     direction.x = +1.0
        elif pressedkeys[K_UP]:        direction.y = -1.0
        elif pressedkeys[K_DOWN]:      direction.y = +1.0
        elif pressedkeys[K_a]:         direction.z = -1.0
        elif pressedkeys[K_q]:         direction.z = +1.0

        if pressedkeys[K_w]:
            fov = min(179.0, fov+1.0)
            viewdistance = calculateViewingDistance( radians(fov), screenwidth)
        elif pressedkeys[K_s]:
            fov = max(1.0, fov-1.0)
            viewdistance = calculateViewingDistance( radians(fov), screenwidth)
        cameraposition += timepassed * cameraspeed * direction
        # draw the 3D points
        for point in points:
            x,y,z = point - cameraposition
            if z > 0:
                x =  x * viewdistance/z
                y = -y * viewdistance/z
                x += centerX
                y += centerY
                screen.blit(ballsurf, (x-ballcenterX,y-ballcenterY) )
        # draw the field of view diagram
        diagramwidth = screenwidth/4
        color = 50,255,50
        diagrampoints = []
        diagrampoints.append( (diagramwidth/2, 100+viewdistance/4) )
        diagrampoints.append( (0,100))
        diagrampoints.append( (diagramwidth,100))
        diagrampoints.append( (diagramwidth/2,100+viewdistance/4))
        diagrampoints.append( (diagramwidth/2,100) )
        pygame.draw.lines(screen,color,False,diagrampoints,2)
        # draw the text
        cam_textsurf = sysfont.render('Camera = %s' %str(cameraposition), True,white)
        fov_textsurf = sysfont.render('field of view = %i' %int(fov), True,white)
        txt = 'viewing distance  = %.3f' % viewdistance
        dist_textsurf = sysfont.render(txt,True,white)
        screen.blit(cam_textsurf, (5,5) )
        screen.blit(fov_textsurf, (5,35) )
        screen.blit(dist_textsurf, (5,65) )
        pygame.display.update()

if __name__ == '__main__':
    main()






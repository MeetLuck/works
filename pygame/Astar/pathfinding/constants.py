from random import random,choice
from colors import *
import pygame

grids = [
        ["   * ",
         " *** ",
         "     ",
         "* ** ",
         "*    "],
        ["     ",
         "  *  ",
         "  *  ",
         "  *  ",
         "     "],
        ]

grid = grids[1]

angle,scale = 0,0.5
imgN = pygame.image.load('arrow-N.png')
imgS = pygame.image.load('arrow-S.png')
imgE = pygame.image.load('arrow-E.png')
imgW = pygame.image.load('arrow-W.png')

imgNEWS = {'N':imgN, 'S':imgS, 'E':imgE, 'W':imgW }
for direction,img in imgNEWS.items():
    img0 = pygame.transform.rotozoom(img,angle,scale)
    imgNEWS[direction] = img0

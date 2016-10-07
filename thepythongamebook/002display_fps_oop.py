'''
002display_fps_pretty.py

Display framerate and playtime

URL    : http://thepythongamebook.com/en:part2:pygame:step002
Author : horst.jens@spielend-programmieren.at
License: GPL, see http://www.gnu.org/licenses/gpl.html
'''

import pygame

class PygView(object):
    def __init__(self,width=640,height=480,fps=30):
        # initialize pygame, window, background, font, ...
        pygame.init()
        pygame.display.set_caption('Press ESC to quit')
        self.width,self.height = width,height
        self.screen = pygame.display.set_mode( (self.width,self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface( self.screen.get_size() ).convert()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono',20,bold=True)
    def run(self):
        # the main loop
        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT: running = False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        running = False


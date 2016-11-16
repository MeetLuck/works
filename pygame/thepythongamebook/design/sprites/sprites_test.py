from sprites import *

class App:
    def __init__(self):
        self.initPygame()
        self.setGroups()
        self.running = True
        Bird()
        self.hunter = BirdCatcher()

    def initPygame(self):
        pygame.init()
        pygame.mixer.pre_init(44100,-16,2,2048)
        screensize = 640,480
        self.screen = pygame.display.set_mode(screensize)
        self.background = pygame.Surface(screensize)
        self.background.fill(white)
        self.background.blit( write('Press LEFT mouse for more sprites'), (5,10) )
        self.background = self.background.convert()
        self.screen.blit(self.background,(0,0))

        Bird.image.append(pygame.image.load('babytux.png'))         # Bird.image[0]
        Bird.image.append(pygame.image.load('babytux_neg.png'))     # Bird.image[1]
        Bird.image.append(Bird.image[0].copy())                   # Bird.image[2]
        # draw blue border
        pygame.draw.rect(Bird.image[2],blue,(0,0,32,36),1)
        for bird in Bird.image:
            bird = bird.convert_alpha()
    def setGroups(self):
        self.birdgroup = pygame.sprite.Group()
        self.allgroup = pygame.sprite.Group()
        Bird.groups = self.birdgroup,self.allgroup
        BirdCatcher.groups = self.allgroup

    def onEvent(self,event):
        if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
            self.running = False

    def onCollision(self):
        for bird in self.birdgroup:
            bird.catched = False
        # --- pygame.sprite.spritecollide(sprite, group,dokill,collided=None) : return Splite_list ---
        crashgroup = pygame.sprite.spritecollide(self.hunter, self.birdgroup,False,pygame.sprite.collide_circle)
        for bird in crashgroup:
            bird.catched = True

    def render(self,seconds):
        self.allgroup.clear(self.screen, self.background)
        self.allgroup.update(seconds)
        self.allgroup.draw(self.screen)
        pygame.display.flip()

    def mainloop(self):
        fps = 60
        clock = pygame.time.Clock()
        seconds = clock.tick(fps)/1000.0
        while self.running:
            for event in pygame.event.get():
                self.onEvent(event)
            if pygame.mouse.get_pressed()[0]:
                Bird(pygame.mouse.get_pos())
            self.onCollision()
            self.render(seconds)

if __name__ == '__main__':
    App().mainloop()

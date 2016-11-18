from lifebar import *

class App:
    def __init__(self):
        self.initPygame()
        self.setGroups()
        self.loadBirdImage()
        self.running = True

    def initPygame(self):
        pygame.init()
        pygame.mixer.pre_init(44100,-16,2,2048)
        screensize = 800,600
        self.screen = pygame.display.set_mode(screensize)
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(white)
        self.background = self.background.convert()
        self.screen.blit(self.background,(0,0))

    def setGroups(self):
        # set sprites group
        self.allgroup = pygame.sprite.LayeredUpdates()
        self.birdgroup = pygame.sprite.Group()
        self.bargroup = pygame.sprite.Group()
        self.catchergroup = pygame.sprite.Group()
        self.fragmentgroup = pygame.sprite.Group()
        Bird.groups = self.birdgroup, self.allgroup
        Lifebar.groups = self.bargroup, self.allgroup
        Fragment.groups = self.fragmentgroup,self.allgroup
        BirdCatcher.groups = self.catchergroup, self.allgroup 

    def loadBirdImage(self):
        Bird.image.append(pygame.image.load(os.path.join('..','babytux.png')) ) # image[0]
        Bird.image.append(pygame.image.load(os.path.join('..','babytux_neg.png')) ) # image[1]
        Bird.image.append(Bird.image[0].copy())  # Bird.image[2]
        Bird.image.append(Bird.image[1].copy())  # Bird.image[3]
        pygame.draw.rect(Bird.image[2],blue,(0,0,32,36),1)
        pygame.draw.rect(Bird.image[3],blue,(0,0,32,36),1)
        for bird in Bird.image:
            bird = bird.convert_alpha()
        self.crysound = pygame.mixer.Sound(os.path.join('..','claws.ogg'))

    def onEvent(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False
    def onMouse(self):
        if pygame.mouse.get_pressed()[0]:
            Bird(self,pygame.mouse.get_pos())
        if pygame.mouse.get_pressed()[2]:
            crashgroup = pygame.sprite.spritecollide(self.hunter, self.birdgroup, True, pygame.sprite.collide_circle)

    def render(self, seconds):
        self.allgroup.clear(self.screen, self.background)
        self.allgroup.update(seconds)
        self.allgroup.draw(self.screen)
        pygame.display.set_caption('Life Bar test')
        pygame.display.flip()

    def quit(self):
        pygame.quit()

    def collision(self):
        for bird in self.birdgroup:
            bird.resetStatus()
        crashgroup = pygame.sprite.spritecollide(self.hunter, self.birdgroup, False,pygame.sprite.collide_circle)
        for crashbird in crashgroup:
            crashbird.catched = True

        for bird in self.birdgroup:
            crashgroup = pygame.sprite.spritecollide(bird,self.birdgroup,False)
            for crashbird in crashgroup:
                if crashbird.number != bird.number:
                    bird.crashing = True
                    bird.Vp -= crashbird.Vp - bird.Vp

    def mainloop(self):
        fps = 60
        clock = pygame.time.Clock()
        self.bird = Bird(self)
        self.hunter = BirdCatcher()
        while self.running:
            seconds = clock.tick(fps)/1000.0
            for event in pygame.event.get():
                self.onEvent(event)
            self.onMouse()
            self.collision()
            self.render(seconds)
        self.quit()

if __name__ == '__main__':
    App().mainloop()

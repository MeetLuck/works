from layer2 import *

class App:
    def __init__(self):
        self.initPygame()
        self.setGroups()
        self.loadImage()
        self.running = True
    def initPygame(self):
        pygame.init()
        pygame.mixer.pre_init(44100,-16,2,2048)
        self.screensize = 640,480
        self.screen = pygame.display.set_mode(self.screensize)
        self.background = pygame.Surface(self.screensize)
        self.background.fill(white)
        self.background = self.background.convert()
        self.screen.blit(self.background,(0,0))
    def loadImage(self):
        Bird.image.append(pygame.image.load('../babytux.png'))
        Bird.image.append(pygame.image.load('../babytux_neg.png'))
        Bird.image.append(Bird.image[0].copy() )
        Bird.image.append(Bird.image[1].copy() )
        pygame.draw.rect(Bird.image[2], green,(0,0,32,36),1)
        pygame.draw.rect(Bird.image[3], red,(0,0,32,36),1)
        for bird in Bird.image:
            bird = bird.convert_alpha()
        self.crysound = pygame.mixer.Sound(os.path.join('..','claws.ogg'))
    def setGroups(self):
        self.allgroup = pygame.sprite.LayeredUpdates()
        self.blockgroup = pygame.sprite.LayeredUpdates()
        self.birdgroup = pygame.sprite.Group()
        self.textgroup = pygame.sprite.Group()
        self.catchergroup = pygame.sprite.Group()
        self.bargroup = pygame.sprite.Group()
        self.fragmentgroup = pygame.sprite.Group()
        self.mountaingroup = pygame.sprite.Group()
        Bird.groups = self.birdgroup, self.allgroup
        Lifebar.groups = self.bargroup, self.allgroup
        Fragment.groups = self.fragmentgroup, self.allgroup
        BirdCatcher.groups = self.catchergroup, self.allgroup
    def onEvent(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False
    def render(self,seconds):
        self.allgroup.clear(self.screen, self.background)
        self.allgroup.update(seconds)
        self.allgroup.draw(self.screen)
        #pygame.display.set_caption('layers')
        pygame.display.flip()
    def quit(self):
        pygame.quit()
    def makeCharacters(self):
        self.hunter = BirdCatcher(self)
        for x in range(self.screen.get_width()//100):
            Block(self,x)
        self.birdlayer = 4
        self.birdtext = Text(self,'current Bird layer = %i' % self.birdlayer)
        for x in range(15):
            Bird(self,self.birdlayer)
        Mountain(self,1)
        Mountain(self,2)
        Mountain(self,3)
    def onMouse(self,seconds):
        if self.cooltime > 0:
            self.cooltime -= seconds
            return
        if pygame.mouse.get_pressed()[0] and self.birdlayer < 10:
            self.birdlayer += 1
            self.cooltime = 0.5
            self.crysound.play()
            for bird in self.birdgroup:
                self.allgroup.change_layer(bird,self.birdlayer)
            for lifebar in self.bargroup:
                self.allgroup.change_layer(lifebar,self.birdlayer)
        if pygame.mouse.get_pressed()[2] and self.birdlayer > -4 :
            self.birdlayer -= 1
            self.cooltime = 0.5
            self.crysound.play()
            for bird in self.birdgroup:
                self.allgroup.change_layer(bird,self.birdlayer)
            for lifebar in self.bargroup:
                self.allgroup.change_layer(lifebar,self.birdlayer)
        pygame.display.set_caption('birds: %i  current layer: %i' %( len(self.birdgroup), self.birdlayer) )
        self.birdtext.newMsg('current bird layer: %i' %self.birdlayer)

    def collision(self):
        if len(self.birdgroup) < 10:
            for x in range(random.randint(1,5)):
                Bird(self,self.birdlayer)
    def mainloop(self):
        fps = 60
        self.cooltime = 0.5
        clock = pygame.time.Clock()
        self.makeCharacters()
        while self.running:
            seconds = clock.tick(fps)/1000.0
            for event in pygame.event.get():
                self.onEvent(event)
            self.onMouse(seconds)
            self.collision()
            self.render(seconds)
        self.quit()

if __name__ == '__main__':
    App().mainloop()

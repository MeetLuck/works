import pygame
white  = pygame.Color('white')
purple = pygame.Color('purple')
class Point:
    def __int__(self,x=None,y=None):
        self.x,self.y = x,y
    def __mul__(self,scalar):
        self.x,self.y = self.x*scalar, self.y*scalar
class Worm:
    def __init__(self,surface):
        self.surface = surface
        self.pos = 0.5 * Point( *surface.get_size() ) 
        self.length = 1
        self.grow_to = 50
        self.v = Point(0,-1)
        self.color = purple
        self.body = list()
        self.crashed = False
    def eat(self):
        self.grow_to += 25
    def event(self,event):
        if event.key == pygame.K_UP:
            self.vx,self.vy = 0, -1
        elif event.key == pygame.K_DOWN:
            self.vx,self.vy = 0,1
        elif event.key == pygame.K_LEFT:
            self.vx,self.vy = -1,0
        elif event.key == pygame.K_RIGHT:
            self.vx,self.vy = 1,0
    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x,self.y in self.body:
            self.crashed = True
        self.body.insert(0, (self.x,self.y))
        if self.grow_to > self.length:
            self.length += 1
        if len(self.body) > self.length:
            self.body.pop()

    def draw(self):
        for x,y in self.body:
            self.surface.set_at( self.pos,self.color)

    def position(self):
        return self.pos

class Food:
    def __init__(self,surface):
        self.surface = surface
        self.pos = Pos()
        self.pos.x = random.randint(0, surface.get_width())
        self.pos.y = random.randint(0, surface.get_height())
        self.color = white
    def draw(self):
        self.surface.set_at( self.pos, self.color)
    def position(self):
        return self.pos

class App:
    w,h = 500,500

    def __init__(self):
        self.screen = pygame.display.set_mode( (self.w,self.h))
        self.clock = pygame.time.Clock()
        self.score = 0
        self.worm = Worm(self.screen)
        self.food = Food(self.screen)
        self.running = True
    def onEvent(self,event):
        self.worm.key_event(event)
    def quit(self):
        pygame.quit()
    def render(self):
        self.worm.draw()
        self.food.draw()
    def mainloop(self):
        while self.running:
            for event in pygame.key.get():
                if event.type == pygame.KEY_DOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                else:
                    self.onEvent(event)
            if self.worm.crashed:
                running = False
            elif h-1 <= self.worm.x <=0:
                running = False
            elif self.worm.position() == self.food.position():
                self.score += 1
                self.worm.eat()
                print 'Score: %d' %score
                self.food = Food(self.screen)
            self.render()


'''
009_02_tile_based_graphic_(improved).py
A simple Maze Wanderer
'''
from constants009 import *

class PygView(object):
    cursorkeys = slice(273,277)
    quitkeys = pygame.K_ESCAPE,pygame.K_q
    events = 'up','down','right','left'

    def __init__(self,controller,config):
        self.controller = controller
        self.width = config.width
        self.height = config.height
        self.bgcolor = config.bgcolor
        self.fps = config.fps
        self.fontcolor = config.fontcolor

        pygame.init()
        # flags
        flags = pygame.DOUBLEBUF | [0,pygame.FULLSCREEN][config.fullscreen]
        self.canvas = pygame.display.set_mode( (self.width,self.height),flags )
        pygame.display.set_caption(config.title)

        self.font = pygame.font.Font(None,self.height/config.fontratio)
        self.clock = pygame.time.Clock()
        # mouse.get_visible
        pygame.mouse.set_visible(config.set_visible)

    @property
    def frameDurationSeconds(self):
        # self.frameDurationSeconds =  0.001 * self.clock.get_time()
        return 0.001 * self.clock.get_time()

    def run(self):
        running = True
        while running:
            # clock.tick_bulsy_loop
            self.clock.tick_busy_loop(self.fps)
            running = self.controller.dispatch(self.getEvents())
            self.flip()
        else: # while ~ else ~
            self.quit()

    def getEvents(self):
        # key.get_pressed
        # cursorkeys = slice(273,277)
        # quitkeys = pygame.K_ESCAPE,pygame.K_q
        # events = 'up','down','right','left'
        keys = pygame.key.get_pressed()[PygView.cursorkeys]
        # [('up',0), ('down',0),'('left',0),'('right',0)]
        move_events = [ event for event,key in zip(PygView.events,keys) if key is True ]
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return 'quit',move_events
            if e.type == pygame.KEYDOWN:
                if e.key in PygView.quitkeys: # K_ESCAPE or K_q
                    return 'quit', move_events
                else:
                    return 'otherkey', move_events
        else: # for else
            return None,move_events

    def drawRect(self,rect,color,border=0):
        pygame.draw.rect(self.canvas,color,rect,border)

    def drawText(self,text):
        fontwidth,fontheight = self.font.size(text)
        textsurf = self.font.render(text,True,self.fontcolor)
        pos =  (self.width - fontwidth)/2, (self.height-fontheight)/2  
        self.canvas.blit(textsurf, pos)
    def flip(self):
        pygame.display.flip()
        self.canvas.fill(self.bgcolor)
    def quit(self):
        pygame.quit()

### class Grid
class Grid(object):
    # calculate points on a rectangular grid
    def __init__(self,dx=1,dy=1,xoff=0,yoff=0):
        self.dx, self.dy = dx,dy   # width,height
        self.xoff, self.yoff = xoff,yoff
    def getPoint(self,x,y):
        return self.xoff + self.dx * x, self.yoff + self.dy * y
    def getRect(self,x,y):
        # return rect = x,y, width, height
        return self.getPoint(x,y) + (self.dx,self.dy)
        # (pointX,pointY) + (self.dx,self.dy) => (pointX,pointY,self.dx,self.dy)
    def getCell(self,x,y):
        # snap coordinates to center point grid
        x,y = int(x+0.5),int(y+0.5)
        return (x-self.xoff+self.dx/2)/self.dx, (y-self.yoff + self.dy/2)/self.dy

### class Map
class Map(object):
    # Maze map representation
    def __init__(self,mapdata):
        self.width,self.height = len(mapdata[0]), len(mapdata)
        self.data = mapdata
    def __getitem__(self,xy):
        x,y = xy
        return self.data[y][x]
    @property
    def startpos(self):
        # search the starting point, there should be only one
        for y,row in enumerate(self.data):
            for x,val in enumerate(y):
                if val == 's': return y,x # s -> start position in the map

### class Mapper(object):
class Mapper(object):
    # manage all maps
    def __init__(self,maps,width,height):
        self.view_width = width
        self.view_height= height
        self.maps = [ Map(m) for m in maps ] # 3 maps -> easy, medium, hard from constants

    def select(self,mode=START): # START = -3 from constants
        assert mode in (START,UP,DOWN,RANDOM),'wrong selection'
        n = len(self.maps) # 3
        #----- select map by self.actindex --> self.maps[actindex]
        if mode == START:
            self.actindex = 0
        elif mode == RANDOM:
            if len(self.maps)>1:
                self.actindex = random.choice( list( set(range(n)) - set([self.actindex]) )  )
        else: # UP,DOWN
            self.actindex = ( self.actindex + n + mode ) % len(self.maps)
        # 
        self.actgrid,self.actcentergrid = self.adjustGrids()
        # actmap: property -> one of self.maps
        return self.actmap, self.actgrid, self.actcentergrid

    def adjustGrids(self):
        # a grid for upper left corner for drawing rectangles,
        # a grid for their center points, which are used for collision detection
        actmap = self.actmap
        width  = self.view_width/actmap.width   - 1
        height = self.view_height/actmap.height - 1
        xoff = self.view_width  - actmap.width * width
        yoff = self.view_height - actmap.height * height

        grid = Grid(width,height,xoff/2,yoff/2)
        centergrid = Grid( width,height, (xoff+width)/2+1,(yoff+height)/2+1  )

        return grid,centergrid

    def drawMap(self,view):
        actmap = self.actmap
        grid = self.actgrid
        width = actmap.width
        for y in range(actmap.height):
            for x in range(width):
                place = actmap[x,y] # __getitem__(self,xy)
                if place not in NOT_DRAWABLES: # constants '.', 's'
                    # mapcolors : constants
                    view.rectangel( gird.getRect(x,y), MAPCOLORS[place], place in places)
    @property
    def actmap(self): # self.actmap = self.maps[...]
        return self.maps[self.actIndex]
    @property
    def startpos(self):
        return self.actmap.startpos
    @property
    def playerSizehint(self):
        return self.actgrid.dx/2,self.actgrid.dy/2
    def getPoint(self,x,y):
        return self.actgrid.getPoint(x,y)
    def getRect(self,x,y):
        return self.actgrid.getRect(x,y)
    def getCell(self,x,y):
        return self.actcentergrid.getCell(x,y)

class Player(object):
    # represent moving player rectangle

    dirs = { 'up':(0,-1), 'down':(0,1),'left':(-1,0),'right':(0,1) }
    sensorpts = [(0,0),(1,0),(1,1),(0,1)]

    def __init__(self,x,y,width,height,color):
        self.x,self.y = x,y
        self.width,self.height = width,height
        self.width2,self.height2 = width/2,height/2
        self.color = color
        self.dx,self.dy = 0,0

    @property
    def pos(self):
        return self.x,self.y
    @property
    def oldPos(self):
        return self.xold,yold
    @property
    def center(self):
        x,y = self.pos
        return x + self.width2, y + self.height2
    @property
    def vertex_sensors(self):
        x,y = self.pos
        return [ (x+sx*self.width, y+ sy*self.height) for sx,sy in Player.sensor_pts ]

    def restorePos(self):
        self.x,self.y = self.oldPos
    def move(self,dt,friction):
        self.dx *= friction
        self.dy *= friction
        self.xold,self.yold = self.pos
        self.x += self.dx * dt
        self.y += self.dy * dt
    def accelerate(self,direct,acc):
        xdir,ydir = Player.dirs(direct)
        self.accx = xdir * acc
        self.accy = ydir * acc
        self.dx += self.accx
        self.dy += self.accy
    def northSensors(self,n):
        x,y = self.pos
        delta = self.width/n
        return [ (x+i*delta,y) for i in range(1,n) ]
    def southSensors(self,n):
        x,y = self.pos
        delta = self.width/n
        h = y + self.height
        return [ (x+i*delta,h) for i in range(1,n) ]
    def westSensors(self,n):
        x,y = self.pos
        delta = self.height/n
        return [ (x, y+i*delta) for i in range(1,n) ]
    def eastSensors(self,n):
        x,y = self.pos
        delta = self.height/n
        w = x + self.width
        return [ (w,y+i*delta) for i in range(1,n) ]
    def bounce(self,west_east, north_south):
        self.dx = (self.dx, -self.dx)[west_east]
        self.dy = (self.dy, -self.dy)[north_south]
    def draw(self,view):
        view.drawRect( (self.x,self.y,self.width,self.height), self.color )

### class Controller
class Controller(object):
    def __init__(self, view, maps, config):
        self.view = view(self,config)
        self.game = MazeGame(maps,config)
        self.game.reset(START) # from constant
        self.state = 'playing'
    def dispatch(self,all_events):
        # control the game state
        # quit or other keys,  move_events  
        event, move_events = all_events
        if event == 'quit':
            self.game.quit()
            return False
        if self.state == 'playing':
            self.state = self.game.process( self.view, move_events )
            return True
        if self.state == 'ending':
            self.game.wait(self.view)
            if event == 'other_key':
                self.state = 'playing'
                self.game.reset(START)
        return True
    def run(self):
        self.view.run()

### class MazeGame
class MazeGame(object):
    def __init__(self,maps,config):
        self.config = config
        self.deltatimer = DeltaTimer(config.dt)
        self.mapper = Mapper(maps, config.width, config.height)
        self.playeraccel = config.playeraccel
        self.friction = config.friction

    def reset(self,mode):
        self.text = ''
        self.mapper.select(mode) # map selection
        x,y = self.mapper.getPoint(*self.mapper.startpos)
        width,height = self.mapper.playerSizehint
        size = self.config.playersize
        width, height = int(width*size), int(height*size)
        self.player = Player(x+1,y+1,width,height, self.config.playercolor)

    def acceleratePlayer(self,events,accel):
        for e in events:
            self.player.accelerate(e, accel)

    def checkPlaces(self):
        place = self.mapper.actmap[ self.mapper.getCell(*self.player.center) ]
        if place in places:
            if place == 'e':
                return 'ending'
            else:
                self.reset( {'u':UP,'d':DOWN,'r':RANDOM}.get(place) )
        return 'playing'

    def checkCollision(self):
        # check at first 4 sides of the player rectangle
        # if collision occurs, check corners
        actmap = self.mapper.actmap
        mapper = self.mapper
        ws = self.config.width_sensors
        hs = self.config.height_sensors
        # x : wall
        north = [ actmap[mapper.getCell(sx,sy) ] == 'x' for sx, sy in self.player.northSensors(ws) ]
        south = [ actmap[mapper.getCell(sx,sy) ] == 'x' for sx, sy in self.player.southSensors(ws) ]
        east  = [ actmap[mapper.getCell(sx,sy) ] == 'x' for sx, sy in self.player.eastSensors(hs) ]
        west  = [ actmap[mapper.getCell(sx,sy) ] == 'x' for sx, sy in self.player.westSensors(hs) ]

        west_east = any(west) or any(east)
        north_south = any(north) or any(south)
        if west_east or north_south:
            self.player.bounce(west_east, north_south)
            return True
        # not weast_east nor north_south
        csx = False
        for sx,sy in self.player.vertex_sensors:
            if actmap[mapper.getCell(sx,sy)] == 'x':
                csx,csy = sy,sy
                break
        if not csx:
            return False

        # csx is True
        old_px,old_py = self.player.oldpos
        px,py = self.player.pos
        oldcsx = csx - px + oldpx
        oldcsy = csy - py + oldpy

        oldcellx,oldcelly = mapper.getCell(oldcsx,oldcsy)
        cellx,celly = mapper.getCell(csx,csy)

        self.player.bounce( abs(oldcellx - cellx) > 0, abs(oldcelly - celly) > 0 )
        return True

    def process(self,view,move_events):
        # main method
        duration = view.frameDurationSeconds
        self.acceleratePlayer(move_events, duration*self.player_accel)
        self.deltatimer += duration
        self.deltatimer.integrate( self.transformPlayer, self.friction)
        self.mapper.drawMap(view)
        self.player.draw(view)
        self.drawText(view)

        return self.check_places()
    def transformPlayer(self,dt,friction):
        # move player in 1 timestep dt
        self.player.move(dt,friction)
        collision = self.checkCollision()
        if collision:
            self.player.restorePos()
            self.player.move(dt,friction)
    def wait(self,view):
        # if player finds exit, ask for new game
        self.text = self.config.waitingtext
        self.drawText(view)
    def drawText(self,view):
        view.drawText(self.text)
    def quit(self):
        print 'Bye'

### class DeltaTimer
class DeltaTimer(object): 
    # Timing control
    def __init__(self,dt):
        self.dt, self.accu = dt,0.0
    def __iadd__(self,delta):
        self.accu += delta
        return self
    def integrate(self,func, *args):
        # for a fixed timestep dt, adjust movement to fps
        while self.accu >= self.dt:
            func(self.dt, * args)
            self.accu -= self.dt

class Config(object):
    # change dictionary to object attribute
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)
def main():
    # maps = easy_map,medium_map, hard_map
    Controller( PygView, maps, Config(**config) ). run()

if __name__ == '__main__':
    main()













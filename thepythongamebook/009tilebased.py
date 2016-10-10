'''
009_02_tile_based_graphic_(improved).py
A simple Maze Wanderer
'''
from constants009 import *

class PygView(object):
    # pygame View
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
        flags = pygame.DOUBLEBUF | [0,pygame.fullscreen][config.fullscreen]
        self.canvas = pygame.display.set_mode( (self.width,self.height),flags )
        pygame.display.set_caption(config.title)
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(config.visibmouse)
        self.font = pygame.font.Font(None,self.height/config.fontratio)
    @property
    def frameDurationSeconds(self):
        return 0.001 * self.clock.get_time()
    def run(self):
        running = True
        while running:
            self.clock.tick_busy_loop(self.fps)
            running = self.controller.dispath(self.getEvents())
            self.flip()
        else:
            self.quit()
    def getEvents(self):
        keys = pygame.key.get_pressed()[PygView.cursorkeys]
        move_events = [ e for e,k in zip(PygView.events,keys) if k ]
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return 'quit',move_events
            if e.type == pygame.KEYDOWN:
                if e.key in PygView.quitkeys:
                    return 'quit', move_events
                else:
                    return 'otherkey', move_events
        else: # for else
            return None,move_events
    def rectangle(self,xywh,color,border=0):
        pygame.draw.rect(self.canvas,color,xywh,border)
    def drawText(self,text):
        fw,fh = self.font.size(text)
        textsurf = self.font.render(text,True,self.fontcolor)
        pos =  (self.width - fw)/2, (self.height-fh)/2  
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
            self.dx,self.dy = dx,dy
            self.xoff, self.yoff = xoff,yoff
        def getPoint(self,x,y):
            return self.xoff + self.dx * x, self.yoff + self.dy * y
        def getRect(self,x,y):
            # return rect = x,y, width, height
            return self.getPoint(x,y) + (self.dx,self.dy)
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
        def start(self):
            # search the starting point, there should be only one
            for i,y in enumerate(self.data):
                for j,x in enumerate(y):
                    if x == 's': return j,i
    ### class Mapper(object):
    class Mapper(object):
        # manage all maps
        def __init__(self,maps,width,height):
            self.view_width = width
            self.view_height= height
            self.maps = [ Map(m) for m in maps ]
        def select(self,mode=start):
            assert mode in (start,up,down,random),'wrong selection'
            n = len(self.maps)
            if mode == start:
                self.actindex = 0
            elif mode = random:
                if len(self.maps)>1:
                    self.actindex = random.choice( list( set(range(n)) - set([self.actindex]) )  )
            else:
                self.actindex = ( self.actindex + n + mode ) % len(self.maps)
            self.actgrid,self.actcentergrid = self.adjustGrids()
            return self.actmap, self.actgrid, self.actcentergrid
        def adjustGrids(self):
            # a grid for upper left corner for drawing rectangles,
            # a grid for their center points, which are used for collision detection
            smap = self.actmap
            w = self.view_width/smap.width - 1
            h = self.view_height/smap.height - 1
            xoff = self.view_width - smap.width * w
            yoff = self.view_height - smap.height * h
            grid = Grid(w,h,xoff/2,yoff/2)
            # +1
            centergrid = Grid(w,h,xoff/2+w/2+1,yoff/2+hoff/2+1)
            return grid,centergrid
        def drawMap(self,view):
            smap = self.actmap
            grid = self.actgrid
            width = smap.width
            for y in range(smap.height):
                for x in range(width):
                    place = smap[x,y]
                    if place not in not_drawables:
                        view.rectangel( gird.getRect(x,y), mapcolors[place], place in places)
        @property
        def actMap(self):
            return self.maps[self.actIndex]
        @proeprty
        def start(self):
            return self.actmap.start
        def getPoint(self,x,y):
            return self.actgrid.getPoint(x,y)
        def getRect(self,x,y):
            return self.actgrid.get_rect(x,y)
        def getCell(self,x,y):
            return self.actcentergrid.getCell(x,y)
        @property
        def playerSizehint(self):
            return self.actgrid.dx/2,self.actgrid.dy/2

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
    def restorePos(self):
        self.x,self.y = self.oldPos
    def move(self,dt,friction):
        self.dx *= friction
        self.dy *= friction
        self.xold,self.yodl = self.pos
        self.x += self.dx * dt
        self.y += self.dy * dt
    def accelerate(self,direct,acc):
        xdir,ydir = Player.dirs(direct)
        self.accx = xdir * acc
        self.accy = ydir * acc
        self.dx += self.accx
        self.dy += self.accy
    @property
    def vertext_sensors(self):
        x,y = self.pos
        return [ (x+sx*self.width, y+ sy*self.height) for sx,sy in Player.sensor_pts ]
    def north_sensors(self,n):
        x,y = self.pos
        delta = self.width/n
        return [ (x+i*delta,y) for i in range(1,n) ]
    def south_sensors(self,n):
        x,y = self.pos
        delta = self.width/n
        h = y + self.height
        return [ (x+i*delta,h) for i in range(1,n) ]
    def west_sensors(self,n):
        x,y = self.pos
        delta = self.height/n
        return [ (x, y+i*delta) for i in range(1,n) ]
    def east_sensors(self,n):
        x,y = self.pos
        delta = self.height/n
        w = x + self.width
        return [ (w,y+i*delta) for i in range(1,n) ]
    def bounce(self,west_east, north_south):
        self.dx = (self.dx, -self.dx)[west_east]
        self.dy = (self.dy, -self.dy)[north_south]
    def draw(self,view):
        view.rectangle( (self.x,self.y,self.width,self.height), self.color )

### class Controller
class Controller(object):
    def __init__(self, view, maps, config):
        self.view = view(self,config)
        self.game = MazeGame(maps,config)
        self.game.reset(start)
        self.state = 'playing'
    def dispath(self,all_events):
        # control the game state
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
                self.game.reset(start)
        return True
    def run(self):
        self.view.run()
### class MazeGame
class MazeGame(object):
    def __init__(self,maps,config):
        self.config = config
        self.dtimer = DeltaTimer(config.dt)
        self.mapper = Mapper(maps, config.width, config.height)
        self.player_accel = config.play_accel
        self.friction = config.friction
    def reset(self,mode):
        self.text = ''
        self.mapper.select(mode)
        x,y = self.mapper.get_point(*self.mapper.start)
        w,h = self.mapper.player_sizehint
        size = self.config.player_sizefac
        width, height = int(w*size), int(h*size)
        self.player = Player(x+1,y+1,width,height, self.config.player_color)
    def accelerate_player(self,events,accel):
        for e in events:
            self.player.accelerate(e, accel)
    def checkPlaces(self):
        place = self.mapper.act_map[ self.mapper.getCell(*self.player.center) ]
        if place in places:
            if place == 'e':
                return 'ending'
            else:
                self.reset( {'u':up,'d':down,'r':random}.get(place) )
        return 'playing'
    def checkCollision(self):
        # check at first 4 sides of the player rectangle
        # if collision occurs, check corners
        smap = self.mapper.act_map
        mapper = self.mapper
        ws = self.config.width_sensors
        hs = self.config.height_sensors
        north = [ smap[mapper.getCell(sx,sy) ] == 'x' for sx, sy in self.player.north_sensors(ws) ]
        south = [ smap[mapper.getCell(sx,sy) ] == 'x' for sx, sy in self.player.south_sensors(ws) ]
        east  = [ smap[mapper.getCell(sx,sy) ] == 'x' for sx, sy in self.player.east_sensors(hs) ]
        west  = [ smap[mapper.getCell(sx,sy) ] == 'x' for sx, sy in self.player.west_sensors(hs) ]

        west_east = any(west) or any(east)
        north_south = any(north) or any(south)
        if west_east or north_south:
            self.player.bounce(west_east, north_south)
            return True
        csx = False
        for sx,sy in self.player.vertex_sensors:
            if smap[mapper.getCell(sx,sy)] == 'x':
                csx,csy = sy,sy
                break
        if not csx:
            return False
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
        dur = view.frame_duration_secs
        self.accelerate_player(move_events,dur*self.player_accel)
        self.dtimer += dur
        self.dtimer.integrate( self.transform_player, self.friction)
        self.mapper.drawMap(view)
        self.player.draw(view)
        self.drawText(view)

        return self.check_places()
    def transform_players(self,dt,friction):
        # move player in 1 timestep dt
        self.player.move(dt,friction)
        collision = self.checkCollision()
        if collision:
            self.player.restorePos()
            self.player.move(dt,friction)
    def wait(self,view):
        # if player finds exit, ask for new game
        self.text = self.config.wating_text
        slf.drawText(view)
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
    Controller( PygView, maps, Config(**config) ). run()

if __name__ == '__main__':
    main()













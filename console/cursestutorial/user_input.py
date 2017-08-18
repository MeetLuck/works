import curses, time
''' more text animation
>>> stdscr = curses.initscr()
>>> dims = stdscr.getmaxyx() 'return a tuple (height,width) of the window'
    row = 0,1,2,...,24
    col = 0,1,2,...,79
>>> stdscr.addstr(row,col,'text',curse.A_REVERSE)  
>>> stdscr.nodelay(1) 'If yes is 1, getch() will be non-blocking.'
'''

from helper import *
import time

class direction(object):
    x = y = 0

class Animation(object):

    def __init__(self,screen):
        self.screen = screen
        self.windows= [self.screen]
        self.init_colors()
        self.screen_instruction()
        self.mainloop(True)

    def screen_instruction(self):
        dimension = ">>> curses.LINES,curses.COLS == stdscr.getmaxyx()"
        rows = ">>> rows = (0,1,2,..,curses.LINES-1)"
        cols = ">>> cols = (0,1,2,..,curses.COLS-1)"
        self.screen.addstr(2,10,'more text animation',self.white)
        self.screen.addstr(3,10,dimension,self.green)
        self.screen.addstr(4,10,rows,self.green)
        self.screen.addstr(5,10,cols,self.green)

    def update(self):
        for win in self.windows:
            win.noutrefresh()
        curses.doupdate()

    def mainloop(self,running):
        # set up window
        rows,cols = 20,50 #curses.COLS-20 #msgwin.getmaxyx()
        msgwin = newwin(rows,cols,7,5,self.green_w)
        #msgwin.nodelay(True)
        self.windows.append(msgwin)
        # initialize variables
        text = 'Hello World'
        row,col = 0,0
        DOWN = RIGHT = +1; UP = LEFT = -1
        # loop
        while running:
            msgwin.erase()
            msgwin.addstr(row,col,text)
            msgwin.addstr(rows-1,cols-6,'{:02},{:02}'.format(row,col),self.red_w)
            self.update()
            time.sleep(0.05)
            q =  msgwin.getch()
            direction.x = direction.y = 0
            if q == 27:
                running = False
            if q == ord('k') and row > 0:
                direction.y = UP
            elif q == ord('j') and row < rows-1:
                direction.y = DOWN
            elif q == ord('h') and col > 0:
                direction.x = LEFT
            elif q == ord('l') and col < cols - len(text):
                direction.x = RIGHT
            row += direction.y
            col += direction.x

if __name__ == '__main__':
    wrapper(Animation)

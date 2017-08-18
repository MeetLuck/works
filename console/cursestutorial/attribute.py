import curses, time
from random import randint
''' Combining Attributes
>>> stdscr = curses.initscr()
>>> dims = stdscr.getmaxyx() 'return a tuple (height,width) of the window'
    row = 0,1,2,...,24 -> max_height = dims[0]-1, max_width = dims[1]-1 
    col = 0,1,2,...,79
>>> stdscr.addstr(row,col,'text',curse.A_REVERSE)  
>>> stdscr.nodelay(1) 'If yes is 1, getch() will be non-blocking.'
>>> stdscr.getch() 'return integer like ord(input)'
>>> curses.curs_set(0) '0:invisible, 1:a underline cursor,2: a block cursor'
    working on windows XP
>>> curses.start_color()
>>> curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(pair_number, fg, bg) 'pair_number=0 reserved'
'''

from helper import *
import time

class Attributes(object):

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
        cursors = ">>> curses.curs_set(0) '0:invisible, 1:a underline cursor, 2:a block cursor'"
        colors = ">>> curses.init_pair(pair_number, fg, bg) pair_number = 0 reserved"
        self.screen.addstr(2,10,'curses colors',self.white)
        self.screen.addstr(3,10,dimension,self.green)
        self.screen.addstr(4,10,rows,self.green)
        self.screen.addstr(5,10,cols,self.green)
        self.screen.addstr(6,10,cursors,self.green)
        self.screen.addstr(7,10,colors,self.green)

    def update(self):
        for win in self.windows:
            win.noutrefresh()
        curses.doupdate()

    def mainloop(self,running):
        # set up window
        rows,cols = 10,curses.COLS-20 #msgwin.getmaxyx()
        b = [curses.A_NORMAL, curses.A_BOLD]
        r = [curses.A_NORMAL, curses.A_REVERSE]
        color_pair = 0
        bold = reverse = 0
        msgwin = newwin(rows,cols,10,10,self.red_w)
        msgwin.box()
        #msgwin.nodelay(True)
        self.windows.append(msgwin)
        # initialize variables
        # loop
        while running:
            ordint = msgwin.getch()
            if ordint == 27:
                running = False
            if ordint in range(49,53):
                color_pair = ordint - 48 
            elif ordint == ord('b'):
                bold = not bold
            elif ordint == ord('r'):
                reverse = not reverse
            attributes = curses.color_pair(color_pair)| b[bold] | r[reverse]
            msgwin.erase()
            msgwin.addstr(randint(0,rows-1),randint(0,cols-1),'A',attributes )
            msgwin.box()
            self.update()
            time.sleep(0.1)

if __name__ == '__main__':
    wrapper(Attributes)

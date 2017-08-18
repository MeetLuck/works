import curses, time
''' basic text animation
>>> stdscr = curses.initscr()
>>> dims = stdscr.getmaxyx() 'return a tuple (height,width) of the window'
    row = 0,1,2,...,24
    col = 0,1,2,...,79
>>> stdscr.addstr(row,col,'text',curse.A_REVERSE)  
>>> window.nodelay(True), 'Non-blocking key'
>>> window.erase(),'Erase old contents of the window'
'''

from helper import *
import time

class Animation(object):

    def __init__(self,screen):
        self.screen = screen
        self.windows= [self.screen]
        self.init_colors()
        self.screen_instruction()
        self.running = True
        self.mainloop()

    def screen_instruction(self):
        nodelay = ">>> window.nodelay(True), 'Non-blocking key'"
        erase = ">>> window.erase(),'Erase old contents of the window'"
        clear = ">>> do NOT use window.clear()"
        self.screen.addstr(2,10,'basic text animation',self.white)
        self.screen.addstr(3,10,nodelay,self.green)
        self.screen.addstr(4,10,erase,self.green)
        self.screen.addstr(5,10,clear,self.brightred)

    def update(self):
        for win in self.windows:
            win.noutrefresh()
        curses.doupdate()

    def mainloop(self):
        rows,cols = 10,curses.COLS-20 #msgwin.getmaxyx()
        msgwin = newwin(rows,cols,7,5,self.green_w)
        self.windows.append(msgwin)
        text = 'Hello World'
        msgwin.nodelay(True)
        self.update()
        col = 0
        RIGHT,LEFT = +1,-1 
        direction = RIGHT
        while self.running:
            msgwin.erase()
            msgwin.addstr(int(rows/2),col,text, curses.A_REVERSE)
            msgwin.box()
            #self.update()
            time.sleep(0.05)
            if msgwin.getch()==27:
                self.running = False
            if col == 0:
                direction = RIGHT
            elif col == cols - len(text):
                direction = LEFT
            col += direction * 1

if __name__ == '__main__':
    wrapper(Animation)

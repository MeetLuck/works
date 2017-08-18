import time
from helper import *


class CLI(object):

    def __init__(self,screen):
        self.screen = screen
        self.init_colors()
        self.screen.bkgd(self.gray)
        self.screen.box()
        self.maxrows,self.maxcols = curses.LINES, curses.COLS #self.screen.getmaxyx()
        self.windows = list()
        self.windows.append(screen)
        self.mainloop()

    def update(self):
        for win in self.windows:
            #win.clear()
            #if win is not self.screen: win.clear()
            win.refresh()

    def mainloop(self):
        winX = newwin(nrows=8,ncols=60,top=5,left=5)
        winY = newwin(nrows=6,ncols=40,top=5+4,left=5-2)
        self.windows.append(winX)
        self.windows.append(winY)
        winX.bkgd(curses.A_REVERSE|self.red)
        winY.bkgd(curses.A_REVERSE|self.brightred)
        winX.addstr('Window X')
        winY.addstr('Window Y')
        msgwin = newwin(nrows=3,ncols=self.maxcols-2,top=self.maxrows-3,left=1) 
        msgwin.bkgd(self.gray)
        msg = 'Press ESC to quit'
        msgwin.addstr(1,self.maxcols/2-len(msg)/2,msg,curses.A_BOLD|self.brightblue)
        self.windows.append(winX)
        self.windows.append(winY)
        self.windows.append(msgwin)
        i=0
        while self.screen.getch() != 27:
            #if ans==27: break
            #winX.erase()
            i = i+1
            winX.erase(); winY.erase()
            winX.box();winY.box()
            winX.addstr(2,3+i,'winX moved')
            winY.addstr(3,3+i,'winY moved')
            self.update()
            time.sleep(0.1)
            if i > 10: 
                #self.screen.clear()
                curses.doupdate(); i = 0#break
            #self.screen.erase()
        else:
            curses.nocbreak(); curses.echo(); curses.curs_set(1)
            curses.endwin()
if __name__ == '__main__':
    wrapper(CLI)

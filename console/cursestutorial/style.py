import curses
''' add string on the terminal
>>> stdscr = curses.initscr()
>>> stdscr.addstr(row,col,'text',curse.A_REVERSE)  
'''

from helper import *

class Style(object):

    def __init__(self,screen):
        self.screen = screen
        self.windows= list()
        self.windows.append(screen)
        self.running = True
        self.init_colors()
        self.mainloop()

    def update(self):
        for win in self.windows:
            win.refresh()

    def mainloop(self):
        self.screen.addstr(2,10,'window.addstr(row,col,text,curses.A_REVERSE)',self.white)
        #self.screen.addstr(2,10,'works only curses.A_REVERSE',self.red)
        msgwin = newwin(10,curses.COLS-10,5,5,self.green_w)
        self.windows.append(msgwin)
        msgwin.addstr(1,5,'Hello World!, curses.A_BLINK',curses.A_BLINK)
        msgwin.addstr(2,5,'Hello World!, curses.A_DIM',curses.A_DIM)
        msgwin.addstr(3,5,'Hello World!')
        msgwin.addstr(4,5,'Hello World!, curses.A_BOLD', curses.A_BOLD)
        msgwin.addstr(5,5,'Hello World!, curses.A_STANDOUT', curses.A_STANDOUT)
        msgwin.addstr(6,5,'Hello World!, curses.A_REVERSE', curses.A_REVERSE)
        msgwin.addstr(7,5,'Hello World!, curses.A_UNDERLINE', curses.A_UNDERLINE)

        while self.running:
            self.update()
            if self.screen.getch():
                self.running = False


if __name__ == '__main__':
    wrapper(Style)

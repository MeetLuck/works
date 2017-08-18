''' moving strings
>>> stdscr = curses.initscr()
>>> dims = stdscr.getmaxyx() 'return a tuple (height,width) of the window'
    row = 0,1,2,...,24
    col = 0,1,2,...,79
>>> stdscr.addstr(row,col,'text',curse.A_REVERSE)  
'''

from helper import *

class Screen(object):

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
        self.screen.addstr(2,10,'stdscr.getmaxyx() == curses.LINES, curses.COLS',self.white)
        dims = self.screen.getmaxyx()
        rows,cols = int(dims[0]/3), dims[1]-10
        msgwin = newwin(rows,cols,5,5,self.green_w)
        msgwin.addstr(rows-2,cols-8,'{},{}'.format(*dims),curses.A_REVERSE)
        string = 'dimension = stdscr.getmaxyx()'
        msgwin.addstr(rows/2,cols/2-len(string)/2,string)
        self.windows.append(msgwin)

        while self.running:
            self.update()
            if self.screen.getch():
                self.running = False


if __name__ == '__main__':
    wrapper(Screen)

#import curses
from helper import *

class MyApp(object):                                                          

    def __init__(self,screen,msg):                                    
        self.screen = screen
        self.msg = msg
        rows,cols = 20,70
        self.window = newwin(rows,cols,5,10)                                  
        self.title = 'this is curses.wrapper example'.center(cols)
        self.quit  = 'Press ESC to quit'.center(cols)
        curses.init_pair(5,curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(6,curses.COLOR_WHITE, curses.COLOR_GREEN)
        self.fg = curses.color_pair(5)
        self.bg = curses.color_pair(6)
        self.window.bkgd(self.bg)
        self.windows = list()
        self.windows.append(screen)
        self.windows.append(self.window)
        self.mainloop()

    def update(self):
        for win in self.windows:
            win.refresh()

    def mainloop(self):                                                       

        while True:                                                          
            self.window.addstr(1,0,self.title,self.fg)
            self.window.addstr(2,5,self.msg)
            self.window.addstr(20-2,0,self.quit,self.fg)
            self.window.box()
            self.update()
            if self.screen.getch()==27: # ESC
                break

if __name__ == '__main__':                                                       
    msg = '''
    def wrapper(callable,*args,**kwargs):
        try:
            stdscr = curses.initscr()
            stdscr.keypad(1)
            curses.noecho(); curses.cbreak(); curses.curs_set(0)
            curses.start_color()
            callable(stdscr,*args,**kwargs)	# Enter the main loop
        finally:
            stdscr.erase()
            stdscr.refresh()
            stdscr.keypad(0)
            curses.echo(); curses.nocbreak(); curses.curs_set(1)
            curses.endwin()			# Terminate curses
            '''
    wrapper(MyApp,msg) #curses.wrapper(MyApp,msg)

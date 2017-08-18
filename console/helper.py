import curses

def wrapper(obj,*args,**kwargs):
    try:
        screen = curses.initscr()
        screen.keypad(1)
        curses.noecho(); curses.cbreak(); curses.curs_set(0)
        curses.start_color()
        setattr(obj,'init_colors',init_colors)
        obj(screen,*args,**kwargs)  # Enter the main loop
    finally:
        screen.clear()
        screen.refresh()
        screen.keypad(0)
        curses.echo(); curses.nocbreak(); curses.curs_set(1)
        curses.endwin()		    # Terminate curses

def init_colors(self):
    # Initialize the color combinations we're going to use
    curses.init_pair(1,1, curses.COLOR_WHITE); curses.init_pair(11,1+8, curses.COLOR_WHITE)
    curses.init_pair(2,2, curses.COLOR_WHITE); curses.init_pair(12,2+8, curses.COLOR_WHITE)
    curses.init_pair(3,3, curses.COLOR_WHITE); curses.init_pair(13,3+8, curses.COLOR_WHITE)
    curses.init_pair(4,4, curses.COLOR_WHITE); curses.init_pair(14,4+8, curses.COLOR_WHITE)
    curses.init_pair(5,5, curses.COLOR_WHITE); curses.init_pair(15,5+8, curses.COLOR_WHITE)
    curses.init_pair(6,6, curses.COLOR_WHITE); curses.init_pair(16,6+8, curses.COLOR_WHITE)
    curses.init_pair(7,7, curses.COLOR_WHITE); curses.init_pair(17,7+8, curses.COLOR_WHITE)
    curses.init_pair(8,8, curses.COLOR_WHITE); 
    self.blue = curses.color_pair(1);     self.brightblue = curses.color_pair(11)
    self.green = curses.color_pair(1);    self.brightgreen = curses.color_pair(12)
    self.cyan = curses.color_pair(3);     self.brightcyan = curses.color_pair(13)
    self.red = curses.color_pair(4);      self.brightred = curses.color_pair(14)
    self.margenta = curses.color_pair(5); self.brightmargenta = curses.color_pair(15)
    self.yellow = curses.color_pair(6);   self.brightyellow = curses.color_pair(16)
    self.white = curses.color_pair(7);    self.brightwhite = curses.color_pair(17)
    self.gray = curses.color_pair(8);     #self.brightgray = curses.color_pair(18)


def newwin(nrows,ncols,top,left):
    assert nrows <= curses.LINES,'out of windows, windows height overflow'
    assert ncols <= curses.COLS, 'out of windows, windows width overflow'
    errormsg = 'out of windows, top <= %s-%s'%(curses.LINES,nrows)
    assert top <= curses.LINES - nrows,errormsg
    window = curses.newwin(nrows,ncols,top,left)
    window.erase()
    window.box()
    return window

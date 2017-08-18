import curses

def wrapper(obj,*args,**kwargs):
    try:
        screen = curses.initscr()
        screen.keypad(1)
        curses.noecho(); curses.cbreak(); curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
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
    self.blue_w = curses.color_pair(1);     self.brightblue_w = curses.color_pair(11)
    self.green_w = curses.color_pair(2);    self.brightgreen_w = curses.color_pair(12)
    self.cyan_w = curses.color_pair(3);     self.brightcyan_w = curses.color_pair(13)
    self.red_w = curses.color_pair(4);      self.brightred_w = curses.color_pair(14)
    self.margenta_w = curses.color_pair(5); self.brightmargenta_w = curses.color_pair(15)
    self.yellow_w = curses.color_pair(6);   self.brightyellow_w = curses.color_pair(16)
    self.white_w = curses.color_pair(7);    self.brightwhite_w = curses.color_pair(17)
    self.gray_w = curses.color_pair(8);     #self.brightgray = curses.color_pair(18)

    curses.init_pair(21,1, -1); curses.init_pair(31,1+8, -1)
    curses.init_pair(22,2, -1); curses.init_pair(32,2+8, -1)
    curses.init_pair(23,3, -1); curses.init_pair(33,3+8, -1)
    curses.init_pair(24,4, -1); curses.init_pair(34,4+8, -1)
    curses.init_pair(25,5, -1); curses.init_pair(35,5+8, -1)
    curses.init_pair(26,6, -1); curses.init_pair(36,6+8, -1)
    curses.init_pair(27,7, -1); curses.init_pair(37,7+8, -1)
    curses.init_pair(28,8, -1); 
    self.black = curses.color_pair(0)
    self.blue = curses.color_pair(21);     self.brightblue = curses.color_pair(31)
    self.green = curses.color_pair(22);    self.brightgreen = curses.color_pair(32)
    self.cyan = curses.color_pair(23);     self.brightcyan = curses.color_pair(33)
    self.red = curses.color_pair(24);      self.brightred = curses.color_pair(34)
    self.margenta = curses.color_pair(25); self.brightmargenta = curses.color_pair(35)
    self.yellow = curses.color_pair(26);   self.brightyellow = curses.color_pair(36)
    self.white = curses.color_pair(27);    self.brightwhite = curses.color_pair(37)
    self.gray = curses.color_pair(28);     #self.brightgray = curses.color_pair(18)


def newwin(nrows,ncols,top,left,color):
    assert nrows <= curses.LINES,'out of windows, windows height overflow'
    assert ncols <= curses.COLS, 'out of windows, windows width overflow'
    errormsg = 'out of windows, top <= %s-%s'%(curses.LINES,nrows)
    assert top <= curses.LINES - nrows,errormsg
    window = curses.newwin(nrows,ncols,top,left)
    window.bkgd(color)
    window.box()
    return window

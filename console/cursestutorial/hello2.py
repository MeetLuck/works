import curses
''' moving strings
>>> stdscr = curses.initscr()
>>> dims = stdscr.getmaxyx() 'return a tuple (height,width) of the window'
    row = 0,1,2,...,24
    col = 0,1,2,...,79
>>> stdscr.addstr(row,col,'text',curse.A_REVERSE)  
'''
stdscr = curses.initscr()
stdscr.clear()
dims = stdscr.getmaxyx()
# row = 0,1,2,...,24  col = 0,1,2,...,79
stdscr.addstr(dims[0]-1,dims[1]-6,'{},{}'.format(*dims),curses.A_REVERSE )
string = 'Hello World!'
# stdscr.addstr(dims[0]/2,dims[1]/2,string)
stdscr.addstr(dims[0]/2,dims[1]/2-len(string)/2,string)
stdscr.refresh()
stdscr.getch()
curses.endwin()


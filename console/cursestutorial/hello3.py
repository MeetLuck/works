import curses, time
''' basic text animation
>>> stdscr = curses.initscr()
>>> dims = stdscr.getmaxyx() 'return a tuple (height,width) of the window'
    row = 0,1,2,...,24
    col = 0,1,2,...,79
>>> stdscr.addstr(row,col,'text',curse.A_REVERSE)  
'''
stdscr = curses.initscr()
dims = stdscr.getmaxyx()
text = 'Hello World!'
for col in range(dims[1]-len(text)):
    stdscr.clear()
    stdscr.addstr(dims[0]/2,col,text,curses.A_BOLD)
    stdscr.refresh()
    time.sleep(0.05)
stdscr.getch()
curses.endwin()


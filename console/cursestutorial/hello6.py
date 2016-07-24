import curses, time
''' Cursor and Move
>>> stdscr = curses.initscr()
>>> dims = stdscr.getmaxyx() 'return a tuple (height,width) of the window'
    row = 0,1,2,...,24 -> max_height = dims[0]-1, max_width = dims[1]-1 
    col = 0,1,2,...,79
>>> stdscr.addstr(row,col,'text',curse.A_REVERSE)  
>>> stdscr.nodelay(1) 'If yes is 1, getch() will be non-blocking.'
>>> stdscr.getch() 'return integer like ord(input)'
>>> curses.curs_set(0) '0:invisible, 1:a underline cursor,2: a block cursor'
    working on windows XP
'''
stdscr = curses.initscr()
curses.noecho()
curses.curs_set(2)
dims = stdscr.getmaxyx()
#dims = stdscr.getmaxyx()
#height = dims[0]-1, width = dims[1]-1
height,width = dims[0]-1, dims[1]-1
text = 'Hello World!'
row,col = 0,0
q = -1
while q != ord('q') :
    stdscr.clear()
    stdscr.addstr(row,col,text)
    stdscr.move(height,width-1)
    stdscr.refresh()
    q = stdscr.getch()
    if q == ord('k') and row > 0: # go UP
        row += -1
    elif q == ord('j') and row < height: # go DOWN
        row += +1
    elif q == ord('h') and col > 0: # go LEFT
        col += -1
    elif q == ord('l') and col < width - len(text): # go RIGHT
        col += +1
    time.sleep(0.01)
curses.endwin()


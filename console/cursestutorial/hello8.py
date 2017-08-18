import curses, time
''' Combining attributes
>>> stdscr = curses.initscr()
>>> dims = stdscr.getmaxyx() 'return a tuple (height,width) of the window'
    row = 0,1,2,...,24 -> max_height = dims[0]-1, max_width = dims[1]-1 
    col = 0,1,2,...,79
>>> stdscr.addstr(row,col,'text',curse.A_REVERSE)  
>>> stdscr.nodelay(1) 'If yes is 1, getch() will be non-blocking.'
>>> stdscr.getch() 'return integer like ord(input)'
>>> curses.curs_set(0) '0:invisible, 1:a underline cursor,2: a block cursor'
    working on windows XP
>>> curses.start_color()
>>> curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(pair_number, fg, bg) 'pair_number=0 reserved'
>>> stdscr.addstr(row,col,'text',curses.color_pair(no)|attr1|attr2|attr3)
'''
stdscr = curses.initscr()
curses.start_color()
curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
curses.init_pair(2,curses.COLOR_BLUE,curses.COLOR_BLACK)
curses.init_pair(3,curses.COLOR_RED,curses.COLOR_BLACK)
curses.init_pair(4,curses.COLOR_CYAN,curses.COLOR_BLACK)
curses.noecho()
stdscr.nodelay(1)
curses.curs_set(2)
dims = stdscr.getmaxyx()
#dims = stdscr.getmaxyx()
#height = dims[0]-1, width = dims[1]-1
height,width = dims[0]-1, dims[1]-1
text = 'Hello!'
vertical,horizontal = 1,1
q = -1
row = col = g = bold = reverse = 0
b = [curses.A_NORMAL, curses.A_BOLD]
r = [curses.A_NORMAL, curses.A_REVERSE]
while q < 0 or q in range(49,53) or q in [98,114]:
    #stdscr.clear()
    q = stdscr.getch()
    if q in range(49,53):
        g = q - 48 
    elif q == 98:
        bold = not bold
    elif q == 114:
        reverse = not reverse
    stdscr.addstr(row,col,str(g),curses.color_pair(g) | b[bold] | r[reverse] )
    row += vertical
    col += horizontal
    if row == height: vertical = -1
    elif row == 0 : vertical = +1
    if col == width - len(text): horizontal = -1
    elif col == 0 : horizontal = +1
    stdscr.refresh()
    time.sleep(0.2)
curses.endwin()

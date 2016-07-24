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
>>> stdscr.keypad(1) 'enable keypad mode'
>>> stdscr.addch(row,col,char,curses.color_pair(no)|attr1|attr2|attr3)
>>> stdscr.delch(row,col)
'''
stdscr = curses.initscr()
stdscr.nodelay(1)
stdscr.keypad(1)
curses.start_color()
curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
curses.init_pair(2,curses.COLOR_BLUE,curses.COLOR_BLACK)
curses.init_pair(3,curses.COLOR_RED,curses.COLOR_BLACK)
curses.init_pair(4,curses.COLOR_CYAN,curses.COLOR_BLACK)
curses.noecho()
curses.curs_set(0)
dims = stdscr.getmaxyx()
#dims = stdscr.getmaxyx()
#height = dims[0]-1, width = dims[1]-1
height,width = dims[0]-1, dims[1]-1
text = 'Hello!'
vertical,horizontal = 1,1
row = col = g = bold = reverse = 0
b = [curses.A_NORMAL, curses.A_BOLD]
r = [curses.A_NORMAL, curses.A_REVERSE]
q = ''
while q != ord('q'):
#   stdscr.clear()
    q = stdscr.getch()
#   if q == ord('q'): break
    if q in range(49,53):
        g = q - 48 
    elif q == 98:
        bold = not bold
    elif q == 114:
        reverse = not reverse
    if row>0 and (q == curses.KEY_UP or q == ord('k')):
        stdscr.delch(row,col)
        row += -1
    elif row<height and ( q == curses.KEY_DOWN or q == ord('j') ):
        stdscr.delch(row,col)
        row += +1
    if col>0 and (q == curses.KEY_LEFT or q == ord('h')):
        stdscr.delch(row,col)
        col += -1
    elif col<width and ( q == curses.KEY_RIGHT or q == ord('l') ):
        stdscr.delch(row,col)
        col += +1
    stdscr.addch(row,col,ord('*'),curses.color_pair(g) | b[bold] | r[reverse] )
    stdscr.refresh()
    time.sleep(0.05)
curses.endwin()

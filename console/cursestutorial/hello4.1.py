import curses, time
''' more text animation
>>> stdscr = curses.initscr()
>>> dims = stdscr.getmaxyx() 'return a tuple (height,width) of the window'
    row = 0,1,2,...,24 -> max_height = dims[0]-1, max_width = dims[1]-1 
    col = 0,1,2,...,79
>>> stdscr.addstr(row,col,'text',curse.A_REVERSE)  
>>> stdscr.nodelay(1) 'If yes is 1, getch() will be non-blocking.'
'''
stdscr = curses.initscr()
stdscr.nodelay(1)
dims = stdscr.getmaxyx()
#dims = stdscr.getmaxyx()
#height = dims[0]-1, width = dims[1]-1
height,width = dims[0]-1, dims[1]-1
text = 'Hello World!'
row,col = 0,0
horizontal,vertical = +1,+1  # + : go down, right  - : go up, left 
q = -1
while q < 0:
    stdscr.clear()
    stdscr.addstr(row,col,text)
    stdscr.refresh()
    row += vertical
    col += horizontal
#   row += 1
#   col += 1
    if row == height:
        vertical = -1
    elif row == 0:
        vertical = +1

    if col == width-len(text):
        horizontal = -1
    elif col == 0:
        horizontal = +1

    q = stdscr.getch()
    time.sleep(0.05)
stdscr.getch()
curses.endwin()


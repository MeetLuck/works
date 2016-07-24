import curses, time
''' more text animation
>>> stdscr = curses.initscr()
>>> dims = stdscr.getmaxyx() 'return a tuple (height,width) of the window'
    row = 0,1,2,...,24
    col = 0,1,2,...,79
>>> stdscr.addstr(row,col,'text',curse.A_REVERSE)  
>>> stdscr.nodelay(1)
'''
stdscr = curses.initscr()
stdscr.nodelay(1)
dims = stdscr.getmaxyx()
#dims = stdscr.getmaxyx()
#height = dims[0]-1, width = dims[1]-1
height,width = dims[0]-1, dims[1]-1
text = 'Hello World!'
x,y = 0,0
horizontal,vertical = 1,1
q = -1
while q < 0:
    stdscr.clear()
    stdscr.addstr(y,x,text)
    stdscr.refresh()
    y += vertical
    x += horizontal
    if y == height:
        vertical = -1
    elif y == 0:
        vertical = 1
    if x == width-len(text):
        horizontal = -1
    elif x == 0:
        horizontal = 1
    q = stdscr.getch()
    time.sleep(0.05)
stdscr.getch()
curses.endwin()


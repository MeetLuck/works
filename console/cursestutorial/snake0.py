import curses, time
''' Border and Movement
>>> screen.border()
'''
screen = curses.initscr()
screen.nodelay(1)
screen.keypad(1)
#screen.border(chr(179),chr(221),chr(196) )
screen.border()
curses.start_color()
curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
curses.noecho()
curses.curs_set(0)
dims = screen.getmaxyx()
#dims = screen.getmaxyx()
#height = dims[0]-1, width = dims[1]-1
height,width = dims[0]-1, dims[1]-1
text = 'Hello!'
vertical,horizontal = 1,1
row = col = g = bold = reverse = 0
b = [curses.A_NORMAL, curses.A_BOLD]
r = [curses.A_NORMAL, curses.A_REVERSE]
q = ''
while q != ord('q'):
#   screen.clear()
    q = screen.getch()
#   if q == ord('q'): break
    if q in range(49,53):
        g = q - 48 
    elif q == 98:
        bold = not bold
    elif q == 114:
        reverse = not reverse
    if row>0 and (q == curses.KEY_UP or q == ord('k')):
        screen.addch(row,col,' ')
        row += -1
    elif row<height and ( q == curses.KEY_DOWN or q == ord('j') ):
        screen.addch(row,col,' ')
        row += +1
    if col>0 and (q == curses.KEY_LEFT or q == ord('h')):
        screen.addch(row,col,' ')
        col += -1
    elif col<width and ( q == curses.KEY_RIGHT or q == ord('l') ):
        screen.addch(row,col,' ')
        col += +1
    screen.addch(row,col,ord('*'),curses.color_pair(g) | b[bold] | r[reverse] )
    screen.refresh()
    time.sleep(0.05)
curses.endwin()

import curses,os
os.system("mode con cols=100 lines=30")
stdscr = curses.initscr()
curses.start_color()
curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
stdscr.addstr(0,0,"Current mode: Normal",curses.color_pair(1))
stdscr.addstr(1,0,"Current mode: Typing", curses.A_REVERSE)
stdscr.addstr(2,0,"Current mode: Bold", curses.A_BOLD)
stdscr.addstr(3,0,"Current mode: Underline not working", curses.A_UNDERLINE)
stdscr.addstr(4,0,"Current mode: Highlight", curses.A_STANDOUT )
#stdscr.border()
stdscr.box()
stdscr.refresh()
nrows,ncols= 10,60
pad = curses.newpad(nrows, ncols)
#pad.box()
# These loops fill the pad with letters; addch() is
# explained in the next section
for y in range(0, nrows-1):
    for x in range(0, ncols-1):
        pad.addch(y,x, ord('a') + (x*x+y*y) % 26)

pad.box()
pad.refresh(0,0, 10,5, 20,75)
# Displays a section of the pad in the middle of the screen.
# (0,0) : coordinate of upper-left corner of pad area to display.
# (5,5) : coordinate of upper-left corner of window area to be filled
#         with pad content.
# (20, 75) : coordinate of lower-right corner of window area to be
#          : filled with pad content.

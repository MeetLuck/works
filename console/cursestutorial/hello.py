import curses
''' add string on the terminal
>>> stdscr = curses.initscr()
>>> stdscr.addstr(row,col,'text',curse.A_REVERSE)  
'''
stdscr = curses.initscr()
stdscr.clear()
stdscr.addstr(0,0,'Hello World!')
stdscr.addstr(1,0,'Hello World!, curses.A_BLINK',curses.A_BLINK)
stdscr.addstr(2,0,'Hello World!, curses.A_DIM',curses.A_DIM)
stdscr.addstr(3,0,'Hello World!, curses.A_BOLD', curses.A_BOLD)
stdscr.addstr(4,0,'Hello World!, curses.A_STANDOUT', curses.A_STANDOUT)
stdscr.addstr(5,0,'Hello World!, curses.A_REVERSE', curses.A_REVERSE)
stdscr.addstr(6,0,'Hello World!, curses.A_UNDERLINE', curses.A_UNDERLINE)
stdscr.refresh()
stdscr.getch()
curses.endwin()


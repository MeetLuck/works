import curses

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.def_prog_mode()
    for i in range(1, curses.COLORS):
        curses.init_pair(i,0,i)
    try:
        for i in range(0, curses.COLORS+20):
            stdscr.addstr(i,0,'%2s: XXXX '%i, curses.color_pair(i))
    except curses.ERR:
        # End of screen reached
        pass
    stdscr.getch()

curses.wrapper(main)

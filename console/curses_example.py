RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
LIGHT_PURPLE = '\033[94m'
PURPLE = '\033[95m'
END = '\033[0m'

def red(name):
    print "\033[91m {0}\033[00m" .format(name)

red('Red color expected')

import curses

def main(stdscr):
    stdscr.clear()
    if curses.has_colors():
        for i in xrange(1, curses.COLORS):
            curses.init_pair(i, i, curses.COLOR_BLACK)
            stdscr.addstr("COLOR %d! " % i, curses.color_pair(i))
            stdscr.addstr("BOLD! ", curses.color_pair(i) | curses.A_BOLD)
            stdscr.addstr("STANDOUT! ", curses.color_pair(i) | curses.A_STANDOUT)
            stdscr.addstr("UNDERLINE! ", curses.color_pair(i) | curses.A_UNDERLINE)
            stdscr.addstr("BLINK! ", curses.color_pair(i) | curses.A_BLINK)
            stdscr.addstr("DIM! ", curses.color_pair(i) | curses.A_DIM)
            stdscr.addstr("REVERSE! ", curses.color_pair(i) | curses.A_REVERSE)
    stdscr.refresh()
    stdscr.getch()

if __name__ == '__main__':
    print "init..."
    curses.wrapper(main)

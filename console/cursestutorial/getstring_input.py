import curses
screen = curses.initscr()
def main(screen):
#   start_color()
#   noecho()
#   curs_set(False)
#   screen.keypad(True)
#   window.addstr(1,1,'Hey window')

#   screen.nodelay(True)
    while True:
        screen.clear()
        screen.refresh()
        curses.curs_set(True)
        curses.echo()
        screen.addstr(5,30, 'Enter command or Press Esc to go back')
        screen.addstr(10,10,'command : ')
        input = screen.getstr(10,21)
        screen.addstr(14,12,input,curses.A_BOLD)
        screen.refresh()
#       curses.curs_set(False)
        curses.noecho()
        screen.addstr(10,20,' '*20)
        screen.move(10,21)
        screen.refresh()
        key = screen.getch()
        if key == 27:
            screen.clear()
            break
    curses.endwin()


if __name__ == '__main__':
    curses.wrapper(main)


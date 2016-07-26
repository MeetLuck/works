''' Changing global variables : Chaning Game Options
>>> screen.inch([row,col] ) 'return a character at row,col'
'''
import curses, time, random

#screen.nodelay(0)
#screen.clear()
#curses.noecho()
#curses.curs_set(0)

def menu():
    from shift import shift
    screen = curses.initscr()
    screen.keypad(1)
    dims = screen.getmaxyx()
    height,width = dims[0]-1, dims[1]-1
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    selection = -1
    opt_string = [' Option : {} '.format(i) for i in range(5) ]
    options = [0] * 5
    options[0] = curses.A_REVERSE
    while True: #selection < 0:
        screen.clear()
        screen.refresh()
        for i in range(len(opt_string)):
            screen.addstr(height/2-len(opt_string)+i,width/2-len(opt_string), opt_string[i],options[i])
        screen.addstr(23,10,'Option : ')
        screen.addstr(23,10+10, str(options.index(curses.A_REVERSE)),curses.color_pair(1)|curses.A_BOLD)
        screen.addstr(23,25,'options : ')
        screen.addstr(23,25+10, str(options), curses.color_pair(2)|curses.A_BOLD)
        screen.addstr(23,60,'selection : ')
        screen.addstr(23,60+12, str(selection), curses.color_pair(2)|curses.A_BOLD)

        action = screen.getch()
        ''' key input processing  '''
        if action == ord('k') or action == curses.KEY_UP: 
            shift(options,-1)
        elif action == ord('j') or action == curses.KEY_DOWN:
            shift(options,1)
        elif action == ord('\n') or action == ord(' '):
            selection = options.index(curses.A_REVERSE)

        ''' selection processing made by SPACE or ENTER  '''
        if selection == 0: pass
        elif selection == 1: pass
        elif selection == 4:
            screen.clear()
            screen.refresh()
            return
menu()

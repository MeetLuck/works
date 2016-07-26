''' Changing global variables : Chaning Game Options
>>> screen.inch([row,col] ) 'return a character at row,col'
'''
import curses, time, random

screen = curses.initscr()
curses.noecho()
dims = screen.getmaxyx()
height,width = dims[0]-1, dims[1]-1
startlength = 8
growlength = 3
speeds = {'Easy':0.1, 'Medium':0.06, 'Hard':0.04 }
difficulty = 'Medium'
acceleration = True
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)


def menu():
    curses.curs_set(0)
    screen.nodelay(0)
    curses.noecho()
    screen.clear()
    screen.keypad(1)
    selection = -1
    option = 1
    opt_string = ['Option : 0','Option : 1','Option : 2','Option : 3','Option : 4']
    while True: #selection < 0:
        screen.clear()
        graphics = [0] * 5
        graphics[option] = curses.A_REVERSE
        for i in range(len(opt_string)):
            screen.addstr(height/2-len(opt_string)+i,width/2-len(opt_string), opt_string[i],graphics[i])
#       screen.addstr(height/2-2,width/2-2, 'Play',graphics[0])
#       screen.addstr(height/2-1,width/2-6, 'Instructions',graphics[1])
#       screen.addstr(height/2,width/2-6, 'Game Options',graphics[2])
#       screen.addstr(height/2+1,width/2-5, 'High Scores',graphics[3])
#       screen.addstr(height/2+2,width/2-2, 'Exit',graphics[4])
        screen.addstr(23,10,'option : ')
        screen.addstr(23,10+10, str(option),curses.color_pair(1)|curses.A_BOLD)
        screen.addstr(23,25,'graphics : ')
        screen.addstr(23,25+10, str(graphics), curses.color_pair(2)|curses.A_BOLD)
        screen.addstr(23,60,'selection : ')
        screen.addstr(23,60+12, str(selection), curses.color_pair(2)|curses.A_BOLD)

        action = screen.getch()
        if action == ord('k'): 
            option = (option-1)%5      # 4->3->2->0->4
        elif action == ord('j'):
            option = (option+1)%5      # 0->1->2->3->4->0
        elif action == ord('\n') or action == ord(' '):
            selection = option
        screen.refresh()
#       screen.clear()
        if selection == 0:
            pass
        elif selection == 1:
            pass
        elif selection == 2:
            pass
menu()

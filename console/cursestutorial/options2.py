''' Adjusting Game Options
>>> screen.inch([row,col] ) 'return a character at row,col'
'''
import curses, time, random


def gameoptions():
    from shift import shift
#   global startlength,growlength,difficulty,acceleration
    screen = curses.initscr()
    dims = screen.getmaxyx()
    height,width = 26,80
    speeds = {'Easy':0.1, 'Medium':0.06, 'Hard':0.04 }
    difficulties = ['Easy','Medium','Hard']
    acceleration = True
    options = [0] * 5
    options[0] = curses.A_REVERSE
    startlengths = range(3,21)
    growlengths = range(1,11)
    startlength, growlength = 8,3
    _start = startlengths.index(startlength)
    _grow = growlengths.index(growlength)
    screen.clear()

    while True:
        startlength = startlengths[_start] # startlength = 8
        growlength = growlengths[_grow]   # grow = 3
        difficulty = difficulties[0]    # difficulty = 'Easy' 
        strings = ['Starting snake length: ' + str(startlength),
                   'Snake Growth rate: ' + str(growlength),
                   'Difficulty: ' + difficulty,
                   'Acceleration: ' + str(acceleration),'Exit']

        screen.refresh()
        for z in range(len(strings)):
            screen.addstr( (height - len(strings))/2 + z, (width -len(strings[z]))/2,strings[z],
                           options[z])
        action = screen.getch()
        screen.clear()
#       screen.refresh()

        if action == ord('k') or action == curses.KEY_UP: 
            shift(options,-1)
        elif action == ord('j') or action == curses.KEY_DOWN:
            shift(options,+1)
        elif action == ord('l') or action == curses.KEY_RIGHT:
            if options.index(curses.A_REVERSE) == 0:  shift(startlengths, -1)
            elif options.index(curses.A_REVERSE)== 1: shift(growlengths,  -1)
        elif action == ord('h') or action == curses.KEY_LEFT:
            if options.index(curses.A_REVERSE) == 0:  shift(startlengths, +1)
            elif options.index(curses.A_REVERSE)== 1: shift(growlengths,  +1)
        elif action == ord('\n') or action == ord(' '):
            curses.flash()
            selection = options.index(curses.A_REVERSE)
            if selection == 2:
                shift(difficulties,-1)
            elif selection == 3:
                acceleration = not acceleration
            elif selection == 4 :
                return

gameoptions()
curses.endwin()




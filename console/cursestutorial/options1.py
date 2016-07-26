''' Adjusting Game Options
>>> screen.inch([row,col] ) 'return a character at row,col'
'''
import curses, time, random


screen = curses.initscr()
dims = screen.getmaxyx()
height,width = dims[0]-1, dims[1]-1
startlength = 8
growlength = 3
speeds = {'Easy':0.1, 'Medium':0.06, 'Hard':0.04 }
difficulty = 'Medium'
acceleration = True

def gameoptions():
    global startlength,growlength,difficulty,acceleration
    screen.clear()
    selection = -1
    option = 0
    while selection < 4:
        graphics = [0] * 5
        graphics[option] = curses.A_REVERSE
        strings = ['Starting snake length: ' + str(startlength),
                   'Snake Growth rate: ' + str(growlength),
                   'Difficulty: ' + difficulty,
                   'Acceleration: ' + str(acceleration),'Exit']

        screen.refresh()
        for z in range(len(strings)):
            screen.addstr( (height - len(strings))/2 + z, (width -len(strings[z]))/2,strings[z],
                           graphics[z])
        action = screen.getch()
        screen.clear()
#       screen.refresh()
        if action == ord('k'):
            option = (option-1)%5
        elif action == ord('j'):
            option = (option+1)%5
        elif action == ord('l'):
            if option == 0 and startlength < 20:
                startlength += 1
            elif option == 1 and growlength < 10:
                growlength += 1
        elif action == ord('h'):
            if option == 0 and startlength >3:
                startlength += -1
            elif option == 1 and startlength > 1:
                growlength +=  -1
        elif action == ord('\n'):
            selection = option

        if selection == 2:
            if difficulty == 'Easy':
                difficulty = 'Medium'
            elif difficulty == 'Medium':
                difficulty = 'Hard'
            elif difficulty == 'Hard':
                difficulty = 'Easy'
        elif selection == 3:
            acceleration = not acceleration
        if selection < 4 :
            selection = -1

gameoptions()
curses.endwin()




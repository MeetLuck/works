''' Changing global variables : Chaning Game Options
>>> screen.inch([row,col] ) 'return a character at row,col'
'''

def menu():
    import curses
    from shift import shift
    screen = curses.initscr()
    screen.keypad(1)
    height,width = 25,80
    selection = -1
    opt_string = [' Option : {} '.format(i) for i in range(5) ]
    options = [0] * 5
    options[0] = curses.A_REVERSE
    while True:
        screen.clear()
        screen.refresh()
        for i in range(len(opt_string)):
            screen.addstr(height/2-len(opt_string)+i,width/2-len(opt_string), opt_string[i],options[i])

        " print option, options, selection "
        screen.addstr(23,10, 'Option: {}'.format(options.index(curses.A_REVERSE)) )
        screen.addstr(23,25, 'Options: {}'.format(options) )
        screen.addstr(23,60, 'Selection: {}'.format(selection) )

        ''' key input processing  '''
        action = screen.getch()
        if action == ord('k') or action == curses.KEY_UP: 
            shift(options,-1)
        elif action == ord('j') or action == curses.KEY_DOWN:
            shift(options,1)
        elif action == ord('\n') or action == ord(' '):
            curses.flash()
            selection = options.index(curses.A_REVERSE)

if __name__ == '__main__':
    menu()

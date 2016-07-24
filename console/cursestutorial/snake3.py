''' Game Over Screen
>>> screen.inch([row,col] ) 'return a character at row,col'
'''
import curses, time, random


def game():
    screen = curses.initscr()
    screen.nodelay(1)
    screen.border()
    curses.noecho()
    curses.curs_set(0)
    dims = screen.getmaxyx()
    height,width = dims[0]-1, dims[1]-1
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    row = col = 2
    head = [row,col]
    body = list()
    deadcell = list()
#   body = [ head[:] ] * 5
#   deadcell = body[-1][:]
    RIGHT,DOWN,LEFT,UP = 0,1,2,3
    direction = RIGHT # 0:right, 1:down, 2:left, 3: up
    gameover = False
    foodmade = False
    length = 5

    while not gameover:

#       if deadcell not in body:
#           screen.addch(deadcell[0],deadcell[1],".")
        while not foodmade:
            pos = random.choice(range(height)),random.choice(range(width))
            if screen.inch(*pos) == ord(' '):
                foodmade = True
                screen.addch(pos[0],pos[1],ord('@') )

        ''' queue
        >>> new -> [ 0->1->2->3->4 ] -> pop
        >>>        [ new->0->1->2->3 ] -> 4
        '''
        body.insert(0,head[:])
        'delete last X'
        if len(body) > length:
            deadcell = body.pop(-1)
            screen.addch(deadcell[0],deadcell[1]," ")
        screen.addch(row,col,ord('X'),curses.color_pair(1)|curses.A_REVERSE )

        action = screen.getch()
        if action == ord('k') and direction != DOWN: # 1
            # action == curses.KEY_UP
            direction = UP # 3
        elif action == ord('j') and direction != UP: # 3
            # action == curses.KEY_DOWN
            direction = DOWN # 1 
        elif action == ord('l') and direction != LEFT: #2
            # action == curses.KEY_RIGHT
            direction = RIGHT  # 2
        elif action == ord('h') and direction != RIGHT:
            # action == curses.KEY_LEFT
            direction = LEFT 

        if   direction == RIGHT:    col += +1
        elif direction == LEFT :    col += -1
        elif direction == DOWN:     row += 1
        elif direction == UP:       row += -1

        head = [row,col]

#       for i in range(len(body)-1,0,-1):
#           body[i] = body[i-1][:]
#       body[0] = head[:]

#       screen.addstr(23,10,str(deadcell),curses.color_pair(0)|curses.A_REVERSE)
#       screen.addstr(23,20,str(body),curses.color_pair(0)|curses.A_REVERSE)

        if screen.inch( *head ) != ord(' '): #head[0],head[1]) != ord(' '):
            if screen.inch( *head) == ord('@'):
                foodmade = False
                body.insert(0,body[0][:])
                length += 1
            else:
                gameover = True
                print 'gameover'
                time.sleep(1)
        screen.move(height,width)
        screen.refresh()
        time.sleep(0.2)
    screen.clear()
    screen.nodelay(0)
    message0 = 'Game Over'
    message1 = 'You got {} point'.format(len(body))
    message2 = 'Press Space to play again'
    message3 = 'Press Enter to quit'
    screen.addstr(height/2-1,(width-len(message0) )/2, message0)
    screen.addstr(height/2 , (width-len(message1) )/2, message1)
    screen.addstr(height/2+1,(width-len(message2) )/2, message2)
    screen.addstr(height/2+2,(width-len(message3) )/2, message3)
    screen.refresh()
    q = screen.getch()
    if q == 32:
        screen.clear()
        game()

game()
curses.endwin()

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

def game():
    screen.clear()
    screen.nodelay(1)
    screen.border()
    curses.noecho()
    curses.curs_set(0)
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
    length = startlength

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
                length += growlength
            else:
                gameover = True
                print 'gameover'
                time.sleep(1)
        screen.move(height,width)
        screen.refresh()
        if not acceleration:
            time.sleep(speeds[difficulty])
        else:
            time.sleep( 15 * speeds[difficulty]/len(body) )

    screen.clear()
    screen.nodelay(0)
    message0 = 'Game Over'
    message1 = 'You got {} point'.format( (len(body)-startlength)/growlength )
    message2 = 'Press Space to play again'
    message3 = 'Press Enter to quit'
    message4 = 'Press M to go to the menu'
    screen.addstr(height/2-1,(width-len(message0) )/2, message0)
    screen.addstr(height/2 , (width-len(message1) )/2, message1)
    screen.addstr(height/2+1,(width-len(message2) )/2, message2)
    screen.addstr(height/2+2,(width-len(message3) )/2, message3)
    screen.addstr(height/2+3,(width-len(message4) )/2, message4)
    screen.refresh()
    q = 0
    while q not in [32,10,77,109]:
        q = screen.getch()
        if q == 32:       # 32 = SPACE bar
            screen.clear()
            game
        elif q in [77,109]: # 77 = m , 109 = M
            screen.clear()
            menu()


def menu():
    curses.curs_set(0)
    screen.nodelay(0)
    curses.noecho()
    screen.clear()
    selection = -1
    option = 0
    while selection < 0:
        graphics = [0] * 5
        graphics[option] = curses.A_REVERSE
        screen.addstr(0,width/2-3, 'Snake')
        screen.addstr(height/2-2,width/2-2, 'Play',graphics[0])
        screen.addstr(height/2-1,width/2-6, 'Instructions',graphics[1])
        screen.addstr(height/2,width/2-6, 'Game Options',graphics[2])
        screen.addstr(height/2+1,width/2-5, 'High Scores',graphics[3])
        screen.addstr(height/2+2,width/2-2, 'Exit',graphics[4])
        action = screen.getch()
        if action == ord('k'): 
            option = (option-1)%5      # 0 1 2 3 4 -> 4,3,2,1,0
        elif action == ord('j'):
            option = (option+1)%5      # 0,1,2,3,4 -> 1,2,3,4,0
        elif action == ord('\n'):
            selection = option
        screen.addstr(23,10,str(option))
        screen.addstr(23,15,str(graphics))
        screen.refresh()
#       screen.clear()
        if selection == 0:
            game()
        elif selection == 1:
            instructions()
        elif selection == 2:
            gameoptions()
def instructions():
    screen.clear()
    screen.nodelay(0)
    tops = ['Snake','By JT']
    centers = ['Use the arrow keys to move', "Don't run into the wall or the snake",
               '','Contact the developer', 'for any questions']
    bottoms = ['Press Any Key', 'to go back to the Menu']
    for z in range(len(tops)):
        screen.addstr( z, (width-len(tops[z]))/2,tops[z])
    for z in range(len(centers)):
        screen.addstr( (height - len(centers))/2 + z, (width -len(centers[z]))/2,centers[z])
    for z in range(len(bottoms)):
        screen.addstr( height+z-len(bottoms), (width-len(bottoms[z]))/2,bottoms[z])
    screen.refresh()
    screen.getch()
    menu()
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

        for z in range(len(strings)):
            screen.addstr( (height - len(strings))/2 + z, (width -len(strings[z]))/2,strings[z],
                           graphics[z])
        screen.refresh()
        action = screen.getch()
        if action == ord('k'):
            option = (option-1)%5
        elif action == ord('j'):
            option = (option+1)%5
        elif action == ord('\n'):
            selection = option
    menu()

# menu()
game()
curses.endwin()

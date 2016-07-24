''' Movement and Control
>>> screen.inch([row,col] ) 'return a character at row,col'
'''
import curses, time, random

def game():
    screen = curses.initscr()
    dims = screen.getmaxyx()
    height,width = dims[0]-1, dims[1]-1
    screen.nodelay(1)
    curses.noecho()
    screen.border()
    head = [3,3]
    body = [ head[:] ] * 5
    deadcell = body[-1][:]
    RIGHT,DOWN,LEFT,UP = 0,1,2,3
    direction = RIGHT # 0:right, 1:down, 2:left, 3: up
    gameover = False

    while not gameover:

#       if deadcell not in body[-1]:
        for cell in body:
            if cell != deadcell:
                screen.addch(deadcell[0],deadcell[1]," ")

        screen.addch(head[0],head[1],ord('X') )

        action = screen.getch()
        if action == ord('k') and direction != 1: # 1
            # action == curses.KEY_UP
            direction = 3 # 3
        elif action == ord('j') and direction != 3: # 3
            # action == curses.KEY_DOWN
            direction = 1 # 1 
        elif action == ord('l') and direction != 2: #2
            # action == curses.KEY_RIGHT
            direction = 0  # 2
        elif action == ord('h') and direction != 0:
            # action == curses.KEY_LEFT
            direction = 2 

        if direction == 0:  #0 
            head[1] += +1
        elif direction == 2: #2
            head[1] += -1
        elif direction == 1: #1
            head[0] += 1
        elif direction == 3:   #3
            head[0] += -1

        deadcell = body[-1][:]
        for i in range(len(body)-1,0,-1):
            body[i] = body[i-1][:]
        body[0] = head[:]

        if screen.inch( *head ) != ord(' '): #head[0],head[1]) != ord(' '):
            gameover = True
        screen.move(height,width)
        screen.refresh()
        time.sleep(0.3)
game()
curses.endwin()



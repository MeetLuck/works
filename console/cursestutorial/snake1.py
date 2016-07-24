''' Border and Movement
>>> screen.inch([row,col] ) 'return a character at row,col'
'''
import curses, time, random

def game():
    screen = curses.initscr()
    screen.nodelay(1)
    screen.border()
    head = [2,2]
    body = [ head[:] ] * 5
    direction = 0
    gameover = False
    while not gameover:
#       screen.addch(head[0],1,'X')
        screen.addch(head[0],head[1],'X')
        if direction == 0:
            head[1] += 1
        elif direction == 2:
            head[1] += -1
        elif direction == 1:
            head[0] += 1
        elif direction == 3:
            head[0] += -1
        if screen.inch( *head ) != ord(' '): #head[0],head[1]) != ord(' '):
            gameover = True
        screen.refresh()
        time.sleep(0.1)
if __name__ == '__main__':
#   curses.wrapper(game)
    game()
    curses.endwin()



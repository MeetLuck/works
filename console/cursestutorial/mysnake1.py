''' Changing global variables : Chaning Game Options
>>> screen.inch([row,col] ) 'return a character at row,col'
'''
import curses, time, random
from shift import shift

screen = curses.initscr()

class Snake(object):
    ''' set global variables'''
    dims = screen.getmaxyx()
    height,width = dims[0]-1, dims[1]-1
    speeds = {'Easy':0.1, 'Medium':0.06, 'Hard':0.04 }
    difficulties = ['Easy','Medium','Hard']
    difficulty = 'Medium'
    acceleration = True
#   options = [0] * 5
#   options[0] = curses.A_REVERSE
    startlength = 8
    growlength = 3
#   length = startlength
    continues = True

    def __init__(self):
        curses.noecho()
        screen.clear()
        screen.nodelay(True)
        screen.border('+','+','-','-')
        curses.curs_set(False)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
        while self.continues:
            len_body = self.play()
            self.gameover(len_body)

    def gameover(self,len_body):
        screen.clear()
        screen.nodelay(False)
        message = range(7)
        message[0] = 'Game Over'
        message[1] = ' '
        message[2] = ['You got ',str( (len_body-self.startlength)/self.growlength), ' point']
        message[3] = ' '
        message[4] = ['Press ','Space',' to Play Again']
        message[5] = ['Press ', 'ESC', ' to Exit']
        message[6] = ['Press ', 'M', ' to go to the Menu']
        screen.addstr(self.height/2-1-3,(self.width-30)/2, message[0].center(30),curses.color_pair(1)|curses.A_REVERSE )
        screen.addstr(self.height/2+0-3, (self.width-30)/2, message[1])

        for j in range(2,7):
            start_pos = self.width/2-25/2
            for i,msg in enumerate(message[j]):
                if i==1:
                    pair_no = 1
                    attr = curses.A_BOLD
                else:
                    pair_no = 0
                    attr = 0
                screen.addstr(self.height/2+j-3 , start_pos, message[j][i],curses.color_pair(pair_no)|attr)
                start_pos += len(msg)

        screen.refresh()


        while True:
            q = screen.getch()
            if q == 32: #in [32,10]: # 32,10 = SPACE bar, Enter
                self.continues = True
                break
            elif q == 27: # ESC
                self.continues = False
                break
            elif q in [77,109]: # 77 = m , 109 = M
                self.menu()
                break
#           return True

    def play(self):
        screen.clear()
        screen.refresh()
        screen.nodelay(True)
        row = col = 2
        head = [row,col]
        body = list()
        deadcell = list()
        RIGHT,DOWN,LEFT,UP = 0,1,2,3
        direction = RIGHT # 0:right, 1:down, 2:left, 3: up
        gameover = foodmade = False
        length = self.startlength


        while not gameover:

            while not foodmade:
                pos = random.choice(range(self.height)),random.choice(range(self.width))
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
            if action == ord('k') and direction != DOWN: # 1 # action == curses.KEY_UP
                direction = UP # 3
            elif action == ord('j') and direction != UP: # 3 # action == curses.KEY_DOWN
                direction = DOWN # 1 
            elif action == ord('l') and direction != LEFT: #2 # action == curses.KEY_RIGHT
                direction = RIGHT  # 2
            elif action == ord('h') and direction != RIGHT: # action == curses.KEY_LEFT
                direction = LEFT 

            if   direction == RIGHT:    col += +1
            elif direction == LEFT :    col += -1
            elif direction == DOWN:     row += +1
            elif direction == UP:       row += -1

            head = [row,col]

            if screen.inch( *head ) != ord(' '): #head[0],head[1]) != ord(' '):
                if screen.inch( *head) == ord('@'):
                    foodmade = False
                    body.insert(0,body[0][:])
                    length += self.growlength
                else:
                    gameover = True
#                   time.sleep(1)
#           screen.move(self.height,self.width)
            screen.refresh()
            if not self.acceleration:
                time.sleep(self.speeds[self.difficulty])
            else:
                time.sleep( 15 * self.speeds[self.difficulty]/len(body) )
        return len(body)


    def menu(self):
        screen = curses.initscr()
        screen.keypad(1)
        opt_string = ['Play', 'Instructions', 'Options', 'High Scores', 'Exit']
        opt_string = [s.center(15) for s in opt_string]
        options = [0] * 5
        options[0] = curses.A_REVERSE
        while True:
            selection = -1
            screen.clear()
            screen.refresh()
            for i in range(len(opt_string)):
                screen.addstr(self.height/2-len(opt_string)+i,self.width/2-len(opt_string), opt_string[i],options[i])

            " print option, options, selection "
            screen.addstr(23,10, 'Option: {}'.format(options.index(curses.A_REVERSE)) )
            screen.addstr(23,25, 'Options: {}'.format(options) )
            screen.addstr(23,60, 'Selection: {}'.format(selection) )

            ''' keybord input processing  '''
            action = screen.getch()
            if action == ord('k') or action == curses.KEY_UP: 
                shift(options,-1)
            elif action == ord('j') or action == curses.KEY_DOWN:
                shift(options,+1)
            elif action == ord('\n') or action == ord(' '):
                curses.flash()
                selection = options.index(curses.A_REVERSE)
            ''' selection '''
            if selection == 0:
                 self.continues = True
                 return
            elif selection == 1:
                self.instructions()
            elif selection == 2:
                self.gameoptions()
            elif selection == 4:
                self.continues = False
                return

    def instructions(self):
        screen.clear()
        screen.nodelay(0)
        tops = ['Snake','By JT']
        centers = ['Use the arrow keys to move', "Don't run into the wall or the snake",
                   '','Contact the developer', 'for any questions']
        bottoms = ['Press Any Key', 'to go back to the Menu']
        for z in range(len(tops)):
            screen.addstr( z, (self.width-len(tops[z]))/2,tops[z])
        for z in range(len(centers)):
            screen.addstr( (self.height - len(centers))/2 + z, (self.width -len(centers[z]))/2,centers[z])
        for z in range(len(bottoms)):
            screen.addstr( self.height+z-len(bottoms), (self.width-len(bottoms[z]))/2,bottoms[z])
        screen.refresh()
        screen.getch()
        self.menu()

    def gameoptions(self):
        screen.clear()
        options = [0] * 5
        options[0] = curses.A_REVERSE
        startlengths = range(3,21)
        growlengths = range(1,11)
        selection = -1
        _start = startlengths.index(self.startlength)
        _grow = growlengths.index(self.growlength)
        while True:
            self.startlength = startlengths[_start] # startlength = 8
            self.growlength = growlengths[_grow]   # grow = 3
            self.difficulty = self.difficulties[0]    # difficulty = 'Easy' 
            strings = ['Starting snake length: ' + str(self.startlength),
                       'Snake Growth rate: ' + str(self.growlength),
                       'Difficulty: ' + self.difficulty,
                       'Acceleration: ' + str(self.acceleration),'Exit']

            screen.refresh()
            for z in range(len(strings)):
                screen.addstr( (self.height - len(strings))/2 + z, (self.width -len(strings[z]))/2,strings[z],
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
                    shift(self.difficulties,-1)
                elif selection == 3:
                    self.acceleration = not self.acceleration
                elif selection == 4 :
                    return

if __name__ == '__main__':
    snake = Snake()
    curses.endwin()

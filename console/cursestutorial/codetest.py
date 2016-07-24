import sys

import time, random
import unicurses as curses 

screen = curses.initscr()
screen.nodelay(1)
screen.border()
curses.noecho()
curses.curs_set(0)
dims = screen.getmaxyx()
height,width = dims[0]-1, dims[1]-1
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

row,col= 0,0
for i in range(256):
    screen.addch(row,col,i,curses.color_pair(0) )
    col +=1
    if col>75:
        row +=1
        col = 1
    screen.refresh()
    time.sleep(0.051)
curses.endwin()

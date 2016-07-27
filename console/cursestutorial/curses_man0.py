import curses
from urllib2 import urlopen
from HTMLParser import HTMLParser
#from simplejson import loads

def get_new_joke():
    return 'aaa'


#   joke_json = loads( urlopen('http://api.icnb.com/jokes/random').read() )
#   return HTMLParser().unescape(joke_json['value']['joke']).encode('cp949')

screen = curses.initscr()
# Property initialize the screen
curses.noecho()
curses.cbreak()
curses.curs_set(0)
# check for and begin color support
if curses.has_colors():
    curses.start_color()
# Optionally enable the
#screen.keypad(1)

# Initialize the color combinations we're going to use
curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2,curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(3,curses.COLOR_RED, curses.COLOR_BLACK)

# BEGIN PROGRAM
screen.addstr('RANMOM QUOTES', curses.A_REVERSE)
screen.chgat(-1, curses.A_REVERSE)
screen.addstr(curses.LINES-1,0, 'Press R to request a new quote, Q to quit')

# Change the R to green
screen.chgat(curses.LINES-1,7,1,curses.A_BOLD|curses.color_pair(2) )
# Change the Q to green
screen.chgat(curses.LINES-1,35,1,curses.A_BOLD|curses.color_pair(1))
# Set up the window to hold the random quotes


quote_window = curses.newwin(curses.LINES-2, curses.COLS,1,0)
#Create a sub-window so as to cleanly display the quote without worrying
# about overwriting the quote windowo's border
quote_text_window = quote_window.subwin(curses.LINES-6, curses.COLS-4,3,2)
quote_text_window.addstr('Press R to get your first quote')
# Draw a border around the main quote window
quote_window.box()
# Update the internal window data structures
screen.noutrefresh()
quote_window.noutrefresh()
# Redraw the screen
curses.doupdate()
# Create the event loop
# Restore the terminal setttings
curses.nocbreak()
curses.echo()
curses.curs_set(1)
# Restore the terminal itself to its 'former glory'
curses.endwin()

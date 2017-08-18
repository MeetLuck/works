import curses,random

def get_new_joke():
    import string
    li = list(string.letters)
    s = random.shuffle(li)
    return ''.join(li)

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
curses.init_pair(2,curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3,curses.COLOR_BLUE, curses.COLOR_BLACK)

# BEGIN PROGRAM
screen.addstr('RANMOM QUOTES', curses.A_REVERSE)
screen.chgat(-1, curses.A_REVERSE)
screen.addstr(curses.LINES-1,0, 'Press R to request a new quote, Q to quit')
height,width = screen.getmaxyx() #curses.LINES, curses.COLS
screen.addstr(height-1,60, "{},{}   {},{}".format(height,width,curses.LINES,curses.COLS) )
screen.addstr(2,10,'xxxxx')
screen.refresh()
screen.getch()

# Change the R to green
screen.chgat(curses.LINES-1,6,1,curses.A_BOLD|curses.color_pair(2) )
# Change the Q to green
screen.chgat(curses.LINES-1,32,1,curses.A_BOLD|curses.color_pair(1))

# Set up the window to hold the random quotes
#curses.newwin(nlines, ncols, begin_row, begin_col)
quote_window = curses.newwin(curses.LINES-4, curses.COLS-4,2,2)

#Create a sub-window so as to cleanly display the quote without worrying
# about overwriting the quote windowo's border
quote_text_window = quote_window.subwin(curses.LINES-6, curses.COLS-6,3,3)
#c8 = ('*',)*8
quote_text_window.addstr(2,2,'Press R to get your first quote')

# Draw a border around the main quote window
quote_text_window.border()
quote_window.border()
#quote_text_window.border(*c8)
#quote_window.border(*tuple('+'*8 ) )

screen.getch()
# Update the internal window data structures
screen.noutrefresh()
quote_window.noutrefresh()
# Redraw the screen
curses.doupdate()

# Create the event loop
while True:
    c = quote_window.getch()
    if c == ord('r') or c == ord('R'):
        quote_text_window.clear()
        quote_text_window.addstr('Gettting quote...', curses.color_pair(3) )
        quote_text_window.refresh()
        quote_text_window.clear()
        quote_text_window.addstr(get_new_joke())
    elif c == ord('q') or c == ord('Q'):
        break

    # Refresh the window from the bottom up
    screen.noutrefresh()
    quote_window.noutrefresh()
    quote_text_window.noutrefresh()
    curses.doupdate()

# Restore the terminal setttings
curses.nocbreak()
curses.echo()
curses.curs_set(1)
# Restore the terminal itself to its 'former glory'
curses.endwin()
                                   
                                   

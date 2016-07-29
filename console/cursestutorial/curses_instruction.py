def myzip(seq1,seq2):
    ''' returned list is truncated to the length of shortest sequence '''
    length = min( len(seq1), len(seq2) )
    result = list()
    for i in range(length):
        t = (seq1[i],seq2[i])
        result.append(t)
    return result    

def get_instruction():
    instructions = [
            '# Propery initialize the screen',
            '# Begin color support',
            '# Optionally enable Keypad',
            "# Initialize the color combinations we're going to use",
            "# BEGIN PROGRAM",
            "# Change the R to green",
            "# Change the Q to red",
            "# Set up the window to hold the random quotes",
            "# set background WHITE",
            "# Draw a border around the main quote window",
            '# Update the internal window data structures',
            '# Redraw the screen',
            '# Create the event loop',
            "    # Refresh the window from the bottom up",
            "# Restore the terminal setttings",
            "# Restore the terminal itself to its 'former glory'",
            ]

    codes = [None]* len(instructions)
    codes[0] = [
            'screen = curses.initscr()',
            'curses.noecho()',
            'curses.cbreak()',
            'curses.curs_set(0)' 
            ]
    codes[1] = [
            'if curses.has_colors():',
            '   curses.start_color()'
            ]
    codes[2] = ['screen.keypad(1)']
    codes[3] = [
            'curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)',
            'curses.init_pair(2,curses.COLOR_GREEN, curses.COLOR_BLACK)',
            'curses.init_pair(3,curses.COLOR_CYAN, curses.COLOR_BLACK)',
            'curses.init_pair(4,curses.COLOR_BLACK, curses.COLOR_WHITE)'
            ]
    codes[4] = [
            "height,width = curses.LINES, curses.COLS",
            "screen.addstr(' '* (width/3) +'RANMOM QUOTES', curses.color_pair(3)|curses.A_REVERSE)",
            "screen.chgat(-1, curses.color_pair(3)|curses.A_REVERSE)",
            "screen.addstr(height-1,0, 'Press R to request a new quote, Q to quit')",
            "screen.addstr(height-1,70, '{},{}'.format(curses.LINES,width) )"
            ]
    codes[5] = [ "screen.chgat(curses.LINES-1,6,1,curses.A_BOLD|curses.color_pair(2) )"]
    codes[6] = [ "screen.chgat(curses.LINES-1,32,1,curses.A_BOLD|curses.color_pair(1))" ]
    codes[7] = [ "quote_window = curses.newwin(curses.LINES-2, curses.COLS-2,1,1)"]
    codes[8] = [ "quote_window.bkgd(curses.color_pair(4))"]
    codes[9] = [
            "quote_window.border(*tuple('+'*8 ) )",
            "quote_window.addstr(1,1,'Press R to get your first quote')",
            ]
    codes[10] = [
            "screen.noutrefresh()",
            "quote_window.noutrefresh()",
            ]
    codes[11] = [ "curses.doupdate()"]
    codes[12] = [
            "while True:",
            "    c = quote_window.getch()",
            "    if c == ord('r') or c == ord('R'):",
            "        quote_window.clear()",
            "        quote_window.addstr(2,2,'Gettting quote...', curses.color_pair(3) )",
            "        quote_window.refresh()",
            "        quote_window.addstr(3,2,get_new_joke())",
            "    elif c == ord('q') or c == ord('Q'):",
            "        break",
            ]
    codes[13] = [
            "    screen.noutrefresh()",
            "    quote_window.noutrefresh()",
            "    curses.doupdate()",
                ]
    codes[14] = [
            "curses.nocbreak()",
            "curses.echo()",
            "curses.curs_set(1)",
            ]
    codes[15] = ["curses.endwin()"]


    # make a list of tuple
    return myzip(instructions,codes)

if __name__ == '__main__':
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    t = get_instruction()
    print
    for instruction, code in t:
        print Fore.GREEN +  instruction
        print Fore.CYAN +  '\n'.join(code)
        print

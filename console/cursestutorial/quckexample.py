import curses
import curses.textpad
stdscr = curses.initscr()
beginX,beginY = 10,5
width,height = 40,20

win = curses.newwin(height,width,beginY,beginX)
win.border()
textbox = curses.textpad.Textbox(win)
#textbox.border()
text = textbox.edit()
curses.addstr(4,1,text.encode('utf_8'))

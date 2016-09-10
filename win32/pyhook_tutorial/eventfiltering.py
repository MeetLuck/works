import pythoncom, pyHook
instructions = '''
- callbacks for key and mouse events can decide whether or not to allow the event
  messages to pass to the windows for which they are intended.
- if a callback function returns True, the message is allowed to pass to callbacks
  registered by other applications and then onto its destination.
- if the function returns False, the message is blocked
'''

def OnKeyboardEvent(event):
    # block only the letter a,A
    return event.Ascii not in (ord('a'),ord('A'))

# create a hook manager
hm = pyHook.HookManager()
# watch for all keyboard events
hm.KeyDown = OnKeyboardEvent
# set up the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()

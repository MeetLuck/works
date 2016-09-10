import pythoncom, pyHook

def OnKeyBoardEvent(event):
    print 'MessageName: ', event.MessageName
    print 'Message: ', event.Message
    print 'Time:', event.Time
    print 'Window: ', event.Window
    print 'Ascii: ', event.Ascii, chr(event.Ascii)
    print 'Key: ', event.Key
    print 'KeyID: ', event.KeyID
    print 'ScanCode: ', event.ScanCode
    print 'Extended: ', event.Extended
    print 'Injected: ', event.Injected
    print 'Alt', event.Alt
    print 'Transition ', event.Transition
    print '-'*80

    # return True to pass the event to ohter handlers
    return True

# create a hook manager
hm = pyHook.HookManager()
# watch for all Keyboard events
hm.KeyDown = OnKeyBoardEvent
# set up the hook
hm.HookKeyboard()
pythoncom.PumpMessages()

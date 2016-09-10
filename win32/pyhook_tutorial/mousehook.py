import pythoncom, pyHook

instructions = '''
- to receive mouse events, you must create a HookManager object and
- provide it will callbacks for the events in which you are interested in.
- you can elect to receive only left button down events, only right button up events,
- only movement events, or all mouse events to name a few.
- each event type can be directed to one and only one callback function
'''
def OnMouseEvent(event):
    # called when mouse events are received
    print 'MessageName: ', event.MessageName
    print 'Message: ', event.Message
    print 'Time: ', event.Time
    print 'WindowName: ', event.WindowName
    print 'Position: ', event.Position
    print 'Wheel: ', event.Wheel
    print 'Injected: ', event.Injected
    print '-'*80

    # return True to pass the event to other handlers
    return True

# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse events
hm.MouseAll = OnMouseEvent
# set up the hook
hm.HookMouse()
# wait forever
pythoncom.PumpMessages()

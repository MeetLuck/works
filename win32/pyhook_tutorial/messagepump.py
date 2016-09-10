import pythocom
pythocom.PumpMessages()
instructions = '''
- Any application that wishes to receive notifications of global input events 
  must have a Windows message pump.
- To get one is to tuse the PumpMessages method in win32 Extenstions.
- when run, this program just sits idle and waits for Windows events.
-> https://sourceforge.net/p/pyhook/wiki/PyHook_Tutorial/#monitoring-global-input-with-pyhook
'''

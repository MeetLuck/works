import sys,pdb

def outer():
    o = 'outer variable'
    inner()

def inner():
    i =  'inner variable'
    frame = sys._getframe(0)
    print frame.f_code
    print frame.f_locals
    frame = sys._getframe(1)
    print frame.f_code
    print frame.f_locals
    frame = sys._getframe(2)
    print frame.f_code
    print frame.f_locals
    #pdb.set_trace()
#   print frame.f_code.co_filename
#   print frame.f_code.co_name
outer()

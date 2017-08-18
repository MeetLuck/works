# 6.18 Automatically Initializing Instance Variables from __init__ Arguments

import inspect
def attributeFromDict(adict):
    print adict
    self = adict.pop('self')
    for name,value in adict.iteritems():
        setattr(self,name,value)

def attributeFromArguments(adict):
    self = adict.pop('self')
    codeObject = self.__init__.im_func.func_code
    argumentNames = codeObject.co_varnames[1:codeObject.co_argcount]
    for name in argumentNames:
        setattr(self,name,adict[name])

class AutoInit(object):
    def __init__(self,foo,bar,boom=1,bang=2):
        self.x = 1
#       print locals()
#       attributeFromDict( locals() )
        attributeFromArguments( locals() )
        print 'self.__dict__ : %s' %self.__dict__
        print 'vars(self): %s' % vars(self)
        print inspect.getargspec(self.__init__)

if __name__ == '__main__':
    a = AutoInit(2,3,boom=10)
    print inspect.getsource(AutoInit.__init__)

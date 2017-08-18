# metaclass how to
# aClass = aMeta.__new__(aMeta,clsname,clsbases,clsdict)
# aMeta.__init__(aClass,clsname,clsbases,clsdict)

import colorama
from colorama import Fore as fg,Back as bg
colorama.init(autoreset=True)

def print_title(color,titlehead,titledata):
    print( color + '{th:14} : {td}'.format(th=titlehead,td=titledata ) )

class supermeta(type):
    def __call__(mcls,clsname,clsbases,clsdict):
        print_title(fg.CYAN,'supermeta.call',mcls)
        clsobj = type.__call__(mcls,clsname,clsbases,clsdict)
        return clsobj

class submeta(type):
    __metaclass__ = supermeta

    def __new__(mcls,clsname,clsbases,clsdict):
#       print fg.CYAN +'<%s.new>' %clsname
#       print '-'*80
#       print fg.CYAN+'mcls:\t',mcls
#       print fg.CYAN+'clsbases:\t',clsbases
#       print fg.CYAN+'clsdict:\n', clsdict
        clsobj =  type.__new__(mcls,clsname,clsbases,clsdict)
#       print fg.CYAN+'aMeta.__new__(...) return',clsobj
        return clsobj

    def __init__(cls,clsname,clsbases,clsdict):
#       print 
#       print fg.GREEN + '%s.init' %clsname
#       print '-'*80
        setattr(cls,'myattr',10)
        setattr(cls,'bar',20)
#       print fg.GREEN+'class:\t',cls
#       print fg.GREEN+'class bases:\t',cls.__bases__
#       print fg.GREEN+'class __dict__:\n',cls.__dict__

    def __call__(cls,*args,**kwargs):
#       print 
#       print fg.YELLOW + 'aMeta.__call__.{cls}({args},{kwargs})'.format(cls=cls,args=args,kwargs=kwargs)
#       print '-'*80
        instance = type.__call__(cls,*args,**kwargs)
#       print fg.YELLOW+'aMeta.__call__ return\t',instance
        return instance

def foo_method(self):
    print( 'foo method in',type(self).__name__ )


class aClass(object):
    __metaclass__ = submeta

    bar = None
    foo = foo_method

    def __new__(cls,*args,**kwargs):
#       print fg.RED + 'aClass.__new__.{cls}({args},{kwargs})'.format(cls=cls,args=args,kwargs=kwargs)
        instance =  object.__new__(cls,*args,**kwargs)
#       print fg.RED +'aClass.__new__ return\t',instance
        return instance

    def __init__(self,*args,**kwargs):
        print( fg.MAGENTA+'aClass.__init__.({self},{args},{kwargs})'.format(self=self,args=args,kwargs=kwargs) )

if __name__ == '__main__':
#   ameta = aMeta()
    aInstance = aClass(2,a=1)
#   print aInstance
#   aClass().show()
#   print aClass.bar
#   print aClass().foo()

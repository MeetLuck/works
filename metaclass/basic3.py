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

class meta(type,metaclass=supermeta):

    def __new__(mcls,clsname,clsbases,clsdict):
        print_title(fg.GREEN,'meta.new',mcls)
        clsobj =  type.__new__(mcls,clsname,clsbases,clsdict)
        return clsobj

    def __init__(cls,clsname,clsbases,clsdict):
        print_title(fg.GREEN,'meta.init',cls)
        setattr(cls,'myattr',10)

    def __call__(cls,*args,**kwargs):
        print_title(fg.GREEN,'meta.call',cls)
        instance = type.__call__(cls,*args,**kwargs)
        return instance

class aClass(metaclass=meta):

    bar = None

    def __new__(cls,*args,**kwargs):
        print_title(fg.YELLOW,'aClass.new',cls)
        instance =  object.__new__(cls) #,*args,**kwargs)
        return instance

    def __init__(self,*args,**kwargs):
        print_title(fg.YELLOW,'aClass.init',self)

if __name__ == '__main__':
    aInstance = aClass(2,a=1)

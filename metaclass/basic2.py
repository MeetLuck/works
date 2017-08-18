import colorama
from colorama import Fore as fg,Back as bg
colorama.init(autoreset=True)

# ---------------------#
#  metaclass skeleton  # 
# ---------------------#

def print_title(color,titlehead,titledata):
    print color + '{th:14} : {td}'.format(th=titlehead,td=titledata ) 

class supermeta(type):
    def __call__(mcls,clsname,clsbases,clsdict):
        print_title(fg.CYAN,'supermeta.call',mcls)
        clsobj = type.__call__(mcls,clsname,clsbases,clsdict)
        return clsobj

class meta(type):
    __metaclass__ = supermeta

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

class aClass(object):
    __metaclass__ = meta

    def __new__(cls,*args,**kwargs):
        print_title(fg.YELLOW,'aClass.new',cls)
        instance =  object.__new__(cls,*args,**kwargs)
        return instance

    def __init__(self,*args,**kwargs):
        print_title(fg.YELLOW,'aClass.init',self)

if __name__ == '__main__':
    anInstance = aClass(2,a=1)
    print anInstance

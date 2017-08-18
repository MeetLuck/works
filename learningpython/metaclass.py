# metaclass how to
# aClass = aMeta.__new__(aMeta,clsname,clsbases,clsdict)
# aMeta.__init__(aClass,clsname,clsbases,clsdict)

import colorama
from colorama import Fore as fg,Back as bg
colorama.init(autoreset=True)

class aMeta(type):
    def __new__(mcls,clsname,clsbases,clsdict):
        clsdict['bar'] = None
        print fg.CYAN +'Allocating memory for class <%s>' %clsname
        print '-'*80
        print 'meta class:\t',mcls
        print 'class bases:\t',clsbases
        print 'class dict:\n', clsdict
        return super(aMeta,mcls).__new__(mcls,clsname,clsbases,clsdict)
    def __init__(cls,clsname,clsbases,clsdict):
#       setattr(cls,'bar',100)
        clsdict.update(bar=10)
#       if 'bar' in clsdict: 
#           print '---------->>'
#           clsdict['bar'] = 10
        print 
        print fg.GREEN + 'Initializing class <%s>' %clsname
        print '-'*80
        print 'class:\t',cls
        print 'class bases:\t',clsbases
        print 'class dict:\n',clsdict
#       super(aMeta,cls).__init__(clsname,clsbases,clsdict)
        type.__init__(cls,clsname,clsbases,clsdict)

def _foo(self,name):
    pass

class aClass(object):
    __metaclass__ = aMeta
#   bar = 2
    foo = _foo

if __name__ == '__main__':
#   aClass()
    print aClass.__dict__
    print aClass.bar

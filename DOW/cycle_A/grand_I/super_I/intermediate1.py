import os,sys
homedir   = os.path.expanduser('~')
elliotdir = os.path.join(homedir,'works\\DOW\\elliot')
sys.path.append(elliotdir)

from helper import *
from elliot70 import *
from toXls import xl

#--------------------------------------------#
#  intermediate I of primaryI(of superI)     #
#--------------------------------------------#

class Intermediate(Impulse):

    def __init__(self,start,end,level,No,has_subwaves=False):
        super(Intermediate,self).__init__(start,end,level,No,has_subwaves)
        if self.has_subwaves:
            self.create_minors()
    def create_minors(self):
        minor1 = Impulse(22180,21840,level=self.level-1,No=1,has_subwaves=True)
        minor2 = ZigZag (21840,22080,level=self.level-1,No=2,has_subwaves=True)
        minor3 = Impulse(22080,None,level=self.level-1,No=3,has_subwaves=True)
        minor4 = ZigZag (None,None,level=self.level-1,No=4,has_subwaves=False)
        minor5 = Impulse (None,None,level=self.level-1,No=5,has_subwaves=False)
        self.set_subwaves(minor1,minor2,minor3,minor4,minor5)
        minor1.create_subwaves(22180,22010,22060,21900,21970,21840,Impulse,Flat,Impulse,Flat,Impulse)
        minor2.create_subwaves(21840,22040,21970,22080,Impulse,Flat,Impulse)
        minor3.create_subwaves(22180,21890,21940,21640,None,None,Impulse,Flat,Impulse,Flat,Impulse)
        #minor3.create_subwaves(22180,21820,21840,None,None,None,Impulse,Flat,Impulse,Flat,Impulse)

intermidate1 = Intermediate(start=22180,end=None,level=-1,No=1,has_subwaves=True)

if __name__ == '__main__':
    book = xl.Workbook()
    #intermidate1.analyze()
    intermidate1.create_xls(book,'intermediate1.xls')
    os.system('start intermediate1.xls')


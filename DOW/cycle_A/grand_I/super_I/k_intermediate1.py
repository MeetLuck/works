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
        minor1 = Impulse(322.75,313.25,level=self.level-1,No=1,has_subwaves=False)
        minor2 = Flat   (313.25,319.45,level=self.level-1,No=2,has_subwaves=False)
        minor3 = Impulse(319.45,None,level=self.level-1,No=3,has_subwaves=True)
        minor4 = ZigZag (None,None,level=self.level-1,No=4,has_subwaves=False)
        minor5 = Impulse (None,None,level=self.level-1,No=5,has_subwaves=False)
        self.set_subwaves(minor1,minor2,minor3,minor4,minor5)
        self.create_minutes(self.iii)
    def create_minutes(self,wave):
        minutes1 = Impulse(319.45,310.80,level=self.level-2,No=1,has_subwaves=False)
        minutes2 = Flat   (310.80,316.30,level=self.level-2,No=2,has_subwaves=False)
        minutes3 = Impulse(316.30,302.30,level=self.level-2,No=3,has_subwaves=False)
        minutes4 = ZigZag (302.30,None,level=self.level-2,No=4,has_subwaves=False)
        minutes5 = Impulse (None,None,level=self.level-2,No=5,has_subwaves=False)
        wave.set_subwaves(minutes1,minutes2,minutes3,minutes4,minutes5)

intermidate1 = Intermediate(start=322.75,end=None,level=-1,No=1,has_subwaves=True)

if __name__ == '__main__':
    book = xl.Workbook()
    intermidate1.analyze()
    intermidate1.create_xls(book,'k_intermediate1.xls')
    os.system('start k_intermediate1.xls')

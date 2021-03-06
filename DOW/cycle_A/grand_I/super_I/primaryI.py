import os,sys
homedir   = os.path.expanduser('~')
elliotdir = os.path.join(homedir,'works\\DOW\\elliot')
sys.path.append(elliotdir)

from helper import *
from elliot70 import *

#------------------------------------#
#  primary I of superI(of GrandV)  #
#------------------------------------#

class Primary(Impulse):

    def __init__(self,start,end,level,No,has_subwaves=False):
        super(Primary,self).__init__(start,end,level,No,has_subwaves)
        if self.has_subwaves:
            self.create_intermediates()
            self.create_minors()
    def create_intermediates(self):
        intermediate1 = Impulse(22180,None,level=self.level-1,No=1,has_subwaves=True)
        intermediate2 = Flat   (None,None,level=self.level-1,No=2,has_subwaves=False)
        intermediate3 = Impulse(None,None,level=self.level-1,No=3,has_subwaves=False)
        intermediate4 = ZigZag (None,None,level=self.level-1,No=4,has_subwaves=False)
        intermediate5 = ZigZag (None,None,level=self.level-1,No=5,has_subwaves=False)
        self.set_subwaves(intermediate1,intermediate2,intermediate3,intermediate4,intermediate5)

    def create_minors(self):
        intermediate1,intermediate2,intermediate3,intermediate4,intermediate5 = self.subwaves
        if intermediate1.has_subwaves:
            intermediate1.create_subwaves(22180,22010,22060,21840,None,None,Impulse,Flat,Impulse,Flat,Impulse)
        if intermediate2.has_subwaves:
            intermediate2.create_subwaves(16511,16287,16664,16165,ZigZag,ZigZag,Impulse)
        if intermediate3.has_subwaves:
            intermediate3.create_subwaves(16165,16795,16510,17648,17399,17811,Impulse,ZigZag,Impulse,Flat,Impulse)
        if intermediate4.has_subwaves:
            intermediate4.create_subwaves(17811,17542,17723,17484,ZigZag,ZigZag,Impulse)
        if intermediate5.has_subwaves:
            intermediate5.create_subwaves(None,None,None,None,None,None,Impulse,ZigZag,Impulse,Flat,Impulse)

primaryI = Primary(start=22180,end=None,level=0,No=1,has_subwaves=True)

if __name__ == '__main__':
    primaryI.analyze()

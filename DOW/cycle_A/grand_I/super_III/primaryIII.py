import os,sys
homedir   = os.path.expanduser('~')
elliotdir = os.path.join(homedir,'works\\DOW\\elliot')
sys.path.append(elliotdir)

from helper import *
from elliot70 import *

#------------------------------------#
#  primary III of superIII(of GrandV)  #
#------------------------------------#

class Primary(Impulse):

    def __init__(self,start,end,level,No,has_subwaves=False):
        super(Primary,self).__init__(start,end,level,No,has_subwaves)
        if self.has_subwaves:
            self.create_intermediates()
            #self.create_minors()

    def create_intermediates(self):
        intermediate1 = Impulse(12471,15658,level=self.level-1,No=1)
        intermediate2 = ZigZag (15658,14760,level=self.level-1,No=2)
        intermediate3 = Impulse(14760,16588,level=self.level-1,No=3)
        intermediate4 = ZigZag (16588,15340,level=self.level-1,No=4)
        intermediate5 = Impulse(15340,17151,level=self.level-1,No=5)
        #intermediate5 = Impulse(15340,17350,level=self.level-1,No=5)
        self.set_subwaves(intermediate1,intermediate2,intermediate3,intermediate4,intermediate5)

    def create_minors(self):
        intermediate1,intermediate2,intermediate3,intermediate4,intermediate5 = self.subwaves
        if intermediate1.has_subwaves:
            intermediate1.create_subwaves(None,None,None,None,None,None,Impulse,ZigZag,Impulse,Flat,Impulse)
        if intermediate2.has_subwaves:
            intermediate2.create_subwaves(None,None,None,None,ZigZag,ZigZag,Impulse)
        if intermediate3.has_subwaves:
            intermediate3.create_subwaves(None,None,None,None,None,None,Impulse,ZigZag,Impulse,Flat,Impulse)
        if intermediate4.has_subwaves:
            intermediate4.create_subwaves(None,None,None,None,ZigZag,ZigZag,Impulse)
        if intermediate5.has_subwaves:
            intermediate5.create_subwaves(None,None,None,None,None,None,Impulse,ZigZag,Impulse,Flat,Impulse)

#primaryIII = Primary(start=12471,end=17350,level=0,No=3,has_subwaves=True)
primaryIII = Primary(start=12471,end=17151,level=0,No=3,has_subwaves=True)

if __name__ == '__main__':
    primaryIII.analyze()

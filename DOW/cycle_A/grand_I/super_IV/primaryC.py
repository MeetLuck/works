import os,sys
homedir   = os.path.expanduser('~')
elliotdir = os.path.join(homedir,'works\\DOW\\elliot')
sys.path.append(elliotdir)

from helper import *
from elliot70 import *

#------------------------------------#
#  primary C of superIV(of GrandV)  #
#------------------------------------#

class Primary(ZigZag):

    def __init__(self,start,end,level,No,has_subwaves=False):
        super(Primary,self).__init__(start,end,level,No,has_subwaves)

        if self.has_subwaves:
            self.create_intermediates()
            #self.create_minors()

    def create_intermediates(self):
        intermediateA = Impulse(17914,17138,level=self.level-1,No=6) # Wedge
        intermediateB = Flat   (17138,17750,level=self.level-1,No=7)
        intermediateC = Impulse(17750,15450,level=self.level-1,No=8)
        self.set_subwaves(intermediateA,intermediateB,intermediateC)

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

primaryC = Primary(start=17914,end=15450,level=0,No=8,has_subwaves=True)

if __name__ == '__main__':
    primaryC.analyze()

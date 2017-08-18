import os,sys
homedir   = os.path.expanduser('~')
elliotdir = os.path.join(homedir,'works\\DOW\\elliot')
sys.path.append(elliotdir)

from helper import *
from elliot70 import *

#------------------------------------#
#  primary IV of superI(of GrandV)  #
#------------------------------------#

class Primary(ZigZag):

    def __init__(self,start,end,level,No,has_subwaves=False):
        super(Primary,self).__init__(start,end,level,No,has_subwaves)
        if self.has_subwaves:
            self.create_intermediates()
            self.create_minors()

    def create_intermediates(self):
        intermediateA = ZigZag (11257,9774,level=self.level-1,No=6,has_subwaves=True)
        intermediateB = Flat   (9774,10593,level=self.level-1,No=7,has_subwaves=True)
        intermediateC = Impulse(10593,9614,level=self.level-1,No=8)
        self.set_subwaves(intermediateA,intermediateB,intermediateC)

    def create_minors(self):
        intermediateA,intermediateB,intermediateC = self.subwaves
        if intermediateA.has_subwaves: # zigzag(5-3-5)
            intermediateA.create_subwaves(11257,9872,10920,9774,Impulse,ZigZag,Impulse)
        if intermediateB.has_subwaves: # flat(3-3-5)
            intermediateB.create_subwaves(9774,10314,9758,10593,ZigZag,ZigZag,Impulse)
        if intermediateC.has_subwaves: # impulse
            intermediateC.create_subwaves(None,None,None,None,None,None,Impulse,ZigZag,Impulse,Flat,Impulse)

primaryIV = Primary(start=11257,end=9614,level=0,No=4,has_subwaves=True)

if __name__ == '__main__':
    primaryIV.analyze()

import os,sys
homedir   = os.path.expanduser('~')
elliotdir = os.path.join(homedir,'works\\DOW\\elliot')
sys.path.append(elliotdir)

from helper import *
from elliot70 import *

#------------------------------------#
#  primary IV of superV(of GrandV)  #
#------------------------------------#

class Primary(ZigZag):

    def __init__(self,start,end,level,No,has_subwaves=False):
        super(Primary,self).__init__(start,end,level,No,has_subwaves)
        if self.has_subwaves:
            self.create_intermediates()
            self.create_minors()

    def create_intermediates(self):
        intermediateA = ZigZag(21169,20412,level=self.level-1,No=6)
        intermediateB = ZigZag(20412,20887,level=self.level-1,No=7)
        intermediateC = ZigZag(20887,20379,level=self.level-1,No=8)
        self.set_subwaves(intermediateA,intermediateB,intermediateC)

    def create_minors(self):
        intermediateA,intermediateB,intermediateC = self.subwaves
        if intermediateA.has_subwaves: # zigzag(5-3-5)
            intermediateA.create_subwaves(None,None,None,None,Impulse,ZigZag,Impulse)
        if intermediateB.has_subwaves: # zigzag(5-3-5)
            intermediateB.create_subwaves(None,None,None,None,ZigZag,ZigZag,Impulse)
        if intermediateC.has_subwaves: # zigzag
            intermediateC.create_subwaves(None,None,None,None,None,None,Impulse,ZigZag,Impulse,Flat,Impulse)

primaryIV = Primary(start=21169,end=20412,level=0,No=4,has_subwaves=True)

if __name__ == '__main__':
    primaryIV.analyze()

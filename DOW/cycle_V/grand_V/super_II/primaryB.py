import os,sys
homedir   = os.path.expanduser('~')
elliotdir = os.path.join(homedir,'works\\DOW\\elliot')
sys.path.append(elliotdir)

from helper import *
from elliot70 import *

#------------------------------------#
#  primary B of superII(of GrandV)  #
#------------------------------------#

class Primary(ZigZag):

    def __init__(self,start,end,level,No,has_subwaves=False):
        super(Primary,self).__init__(start,end,level,No,has_subwaves)
        if self.has_subwaves:
            self.create_intermediates()
            #self.create_minors()

    def create_intermediates(self):
        intermediateA = Impulse(11555,12450,level=self.level-1,No=6)
        intermediateB = ZigZag (12450,12093,level=self.level-1,No=7)
        intermediateC = Impulse(12093,12875,level=self.level-1,No=8)
        self.set_subwaves(intermediateA,intermediateB,intermediateC)

#   def create_minors(self):
#       intermediateA,intermediateB,intermediateC = self.subwaves
#       if intermediateA.has_subwaves: # zigzag(5-3-5)
#           intermediateA.create_subwaves(18167,17580,17934,17331,Impulse,ZigZag,Impulse)
#       if intermediateB.has_subwaves: # zigzag(5-3-5)-zigzag(5-flat-5)-impulse
#           intermediateB.create_subwaves(17331,17899,17471,18011,ZigZag,ZigZag,Impulse)
#       if intermediateC.has_subwaves: # unidentified
#           intermediateC.create_subwaves(None,None,None,None,None,None,Impulse,ZigZag,Impulse,Flat,Impulse)

primaryB = Primary(start=11555,end=12875,level=0,No=7,has_subwaves=True)

if __name__ == '__main__':
    primaryB.analyze()

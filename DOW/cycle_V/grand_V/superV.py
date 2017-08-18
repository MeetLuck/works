import os,sys
homedir   = os.path.expanduser('~')
elliotdir = os.path.join(homedir,'works\\DOW\\elliot')
sys.path.append(elliotdir)

from elliot70 import *
from super_V import * # from superV import primaryII

#------------------------------------#
#  superV of GrandV(of CycleV)  #
#------------------------------------#

class SuperV(Impulse):

    def __init__(self,start,end,level,No,has_subwaves=False):
        super(SuperV,self).__init__(start,end,level,No,has_subwaves)
        if self.has_subwaves:
            self.set_subwaves(primaryI,primaryII,primaryIII,primaryIV,primaryV)

superV = SuperV(start=15503,end=None,level=+1,No=5,has_subwaves=True)

if __name__ == '__main__':
    superV.analyze()

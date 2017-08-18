import os,sys
homedir   = os.path.expanduser('~')
elliotdir = os.path.join(homedir,'works\\DOW\\elliot')
sys.path.append(elliotdir)

from elliot70 import *
from super_II import * # from superV import primaryII

#------------------------------------#
#  superII of GrandV(of CycleV)  #
#------------------------------------#

class SuperII(Flat):

    def __init__(self,start,end,level,No,has_subwaves=False):
        super(SuperII,self).__init__(start,end,level,No,has_subwaves)
        if self.has_subwaves:
            self.set_subwaves(primaryA,primaryB,primaryC)

superII = SuperII(start=12391,end=10404,level=+1,No=2,has_subwaves=True)

if __name__ == '__main__':
    superII.analyze()

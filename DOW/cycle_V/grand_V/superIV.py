import os,sys
homedir   = os.path.expanduser('~')
elliotdir = os.path.join(homedir,'works\\DOW\\elliot')
sys.path.append(elliotdir)

from elliot70 import *
from super_IV import * # from superV import primaryII

#------------------------------------#
#  superIV of GrandV(of CycleV)  #
#------------------------------------#

class SuperIV(Flat):

    def __init__(self,start,end,level,No,has_subwaves=False):
        super(SuperIV,self).__init__(start,end,level,No,has_subwaves)
        if self.has_subwaves:
            self.set_subwaves(primaryA,primaryB,primaryC)

superIV = SuperIV(start=18351,end=15450,level=+1,No=4,has_subwaves=True)

if __name__ == '__main__':
    superIV.analyze()

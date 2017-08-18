import os,sys
homedir   = os.path.expanduser('~')
elliotdir = os.path.join(homedir,'works\\DOW\\elliot')
sys.path.append(elliotdir)

from elliot70 import *
from super_III import * # from superV import primaryII

#------------------------------------#
#  superIII of GrandV(of CycleV)  #
#------------------------------------#

class SuperIII(Impulse):

    def __init__(self,start,end,level,No,has_subwaves=False):
        super(SuperIII,self).__init__(start,end,level,No,has_subwaves)
        if self.has_subwaves:
            self.set_subwaves(primaryI,primaryII,primaryIII,primaryIV,primaryV)

superIII = SuperIII(start=10404,end=18351,level=+1,No=3,has_subwaves=True)

if __name__ == '__main__':
    superIII.analyze()

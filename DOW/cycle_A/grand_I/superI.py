import os,sys
homedir   = os.path.expanduser('~')
elliotdir = os.path.join(homedir,'works\\DOW\\elliot')
sys.path.append(elliotdir)

from elliot70 import *
from super_I import * # from superV import primaryII

#------------------------------------#
#  superI of GrandV(of CycleV)  #
#------------------------------------#

class SuperI(Impulse):

    def __init__(self,start,end,level,No,has_subwaves=False):
        super(SuperI,self).__init__(start,end,level,No,has_subwaves)
        if self.has_subwaves:
            self.set_subwaves(primaryI,primaryII,primaryIII,primaryIV,primaryV)

superI = SuperI(start=6470,end=12391,level=+1,No=1,has_subwaves=True)

if __name__ == '__main__':
    superI.analyze()

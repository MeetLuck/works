import os,sys
homedir   = os.path.expanduser('~')
elliotdir = os.path.join(homedir,'works\\DOW\\elliot')
sys.path.append(elliotdir)

from elliot70 import *
from grand_V import * 
from toXls import WaveToXls,xl

#------------------------------------#
#          grandV of CycleV          #
#------------------------------------#

class GrandV(Impulse):

    def __init__(self,start,end,level,No,has_subwaves=False):
        super(GrandV,self).__init__(start,end,level,No,has_subwaves)
        assert self.has_subwaves,'no Super Waves found'
        self.set_subwaves(superI,superII,superIII,superIV,superV)

grandV = GrandV(start=6470,end=None,level=+2,No=5,has_subwaves=True)

if __name__ == '__main__':
    #grandV.analyze()
    book = xl.Workbook()
    grandV.create_xls(book,'grandV.xls')
    import os,sys
    os.system('start grandV.xls')

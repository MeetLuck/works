import os,sys
homedir   = os.path.expanduser('~')
elliotdir = os.path.join(homedir,'works\\DOW\\elliot')
sys.path.append(elliotdir)

from elliot70 import *

#------------------------------------#
#  primary V of superI(of GrandV)  #
#------------------------------------#

class Primary(Impulse):

    def __init__(self,start,end,level,No,has_subwaves=False):
        super(Primary,self).__init__(start,end,level,No,has_subwaves)
        if self.has_subwaves:
            self.create_intermediates()
            #self.create_minors()

    def create_intermediates(self):
        intermediate1 = Impulse(9614,10719,level=-1,No=1)  # Diagonal
        intermediate2 = ZigZag (10719,9936,level=-1,No=2)
        intermediate3 = Impulse(9936,11451,level=-1,No=3)
        intermediate4 = ZigZag (11451,10929,level=-1,No=4)
        intermediate5 = Impulse(10929,12391,level=-1,No=5)
        self.set_subwaves(intermediate1,intermediate2,intermediate3,intermediate4,intermediate5)

    def create_minors(self):
        intermediate1,intermediate2,intermediate3,intermediate4,intermediate5 = self.subwaves
        if intermediate1.has_subwaves:
            intermediate1.create_subwaves(None,None,None,None,None,None,Impulse,ZigZag,Impulse,Flat,Impulse)
        if intermediate2.has_subwaves:
            intermediate2.create_subwaves(None,None,None,None,ZigZag,ZigZag,Impulse)

        if intermediate3.has_subwaves: # running triangle
            #intermediate3.create_subwaves(None,None,None,None,None,None,Impulse,ZigZag,Impulse,Flat,Impulse)
            # ---------- case II -----------------------------------------------
            intermediate3.create_subwaves(20553,21112,20942,21225,21186,21535,Impulse,ZigZag,Impulse,Flat,Impulse)

        if intermediate4.has_subwaves:
            intermediate4.create_subwaves(None,None,None,None,ZigZag,ZigZag,Impulse)
        if intermediate5.has_subwaves:
            intermediate5.create_subwaves(None,None,None,None,None,None,Impulse,ZigZag,Impulse,Flat,Impulse)


primaryV = Primary(start=9614,end=12391,level=0,No=5,has_subwaves=True)

if __name__ == '__main__':
    primaryV.analyze()

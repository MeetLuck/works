import os,sys
homedir   = os.path.expanduser('~')
elliotdir = os.path.join(homedir,'works\\DOW\\elliot')
sys.path.append(elliotdir)

from elliot70 import *

#------------------------------------#
#  primary V of superV(of GrandV)  #
#------------------------------------#

class Primary(Impulse):

    def __init__(self,start,end,level,No,has_subwaves=False):
        super(Primary,self).__init__(start,end,level,No,has_subwaves)
        if self.has_subwaves:
            self.create_intermediates()
            self.create_minors()

    def create_intermediates(self):
        intermediate1 = Impulse(20379,20938,level=-1,No=1)
        intermediate2 = Flat   (20938,20553,level=-1,No=2)
        # ---------- case I -----------------------------------------------
        #intermediate3 = Impulse(20553,21225,level=-1,No=3)
        #intermediate4 = Flat   (21225,21186,level=-1,No=4)
        #intermediate5 = Impulse(21186,None,level=-1,No=5)
        # ---------- case II -----------------------------------------------
        intermediate3 = Impulse(20553,21535,level=-1,No=3,has_subwaves=True)
        intermediate4 = Flat   (21535,21200,level=-1,No=4)
        intermediate5 = Impulse(21200,None,level=-1,No=5)
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


primaryV = Primary(start=20379,end=None,level=0,No=5,has_subwaves=True)

if __name__ == '__main__':
    primaryV.analyze()

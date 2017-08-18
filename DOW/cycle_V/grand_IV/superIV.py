# Elliot Wave Analysis [IV] #
#   start       wave I         wave II         wave III        wave IV         wave V
# 6450(0) -> 12391(+5951) -> 10404(-1987) -> 18351(+7906) -> 15450(-2906) -> 20401?(+5941?)

import sys
sys.path.append('../elliot')

from elliot60 import *

class superIV(Flat):
    def __init__(self):
        super(superIV,self).__init__(start=11750, end=6450, level=+1, No=4) 
        self.create_subwaves(11750,7197,14198,6450,Flat,ZigZag,Impulse)
        self.set_primaries()
    def set_primaries(self):
        # wave A   : 11750 - 8062(a) - 10673(b) - 7197(c)   # Flat(3-3-5)
        # wave B   : 7197  - 10753(a) - 10200(b) - 14198(c) # ZigZag(5-T-5)  
        # wave C   : 14198 - 11730(p1) - 13139(p2) - 7450(p3) - 9088(p4) - 6450(p5)
        self.a.create_subwaves(11750,8062,10673,7197,Flat,Flat,Impulse) # Flat - Flat - Impulse
        self.b.create_subwaves(7197,10753,10200,14198,Impulse,Triangle,Impulse) # 5-Triangle-5
        self.c.create_subwaves(14198,11730,13139,7450,9088,6450,Impulse,ZigZag,Impulse,ZigZag,Impulse)
    def analyze(self):
        print_title(fg.RED,'super-wave {name}'.format(name=self.name))
        overview(self)
        for primary in self.subwaves:
            print_title(fg.BLUE,'primary {name} Analysis'.format(name=primary.name))
            overview(primary)
            if primary.No != 8: continue
            print_fibs(primary)
            print_predictions(primary)

if __name__ == '__main__':
    superiv = superIV()
    superiv.analyze()

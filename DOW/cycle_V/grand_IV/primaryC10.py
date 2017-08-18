# Primary Wave C of [IV] #
#   start    wave I    wave II   wave III   wave IV    wave V
#   14198    11730     13139     7450       9088       6450  

import sys
sys.path.append('../elliot')

from elliot60 import *

class PrimaryC(Impulse):
    def __init__(self):
        super(PrimaryC,self).__init__(start=14198, end=6450, level=0, No=8)
        self.create_intermediates()
        self.create_minors()
    def create_intermediates(self):
        self.create_subwaves(14198,11730,13139,7450,9088,6450,Impulse,ZigZag,Impulse,ZigZag,Impulse)
    def create_minors(self):
        # intermediate i(minor i, minor ii,...)   : 14198,12724,13778,12069,12756,11731
        # intermediate ii(minor a, minor b,...)   : 11732,12621,12269,13136            -> ZigZag
        # intermediate iii(minor i, minor ii,...) : 13139,10827,11874,8130,9654,7450 
        # intermediate iv(minor a, minor b,...)   : 7450,8828,8118,8961,8364,9087      ->Triangle
        # intermediate v(minor i, minor ii,...)   : 9087,7909,8314,7106,7404,6470 
        self.i.create_subwaves(14198,12724,13778,12069,12756,11731,Impulse,ZigZag,Impulse,ZigZag,Impulse)
        self.ii.create_subwaves(11732,12621,12269,13136,Impulse,ZigZag,Impulse)
        self.iii.create_subwaves(13139,10827,11874,8130,9654,7450,Impulse,Flat,Impulse,ZigZag,Impulse)
        self.iv.create_subwaves(7450,9026,8364,9087,ZigZag,ZigZag,Impulse)
        self.v.create_subwaves(14198,12724,13778,12069,12756,11731,Impulse,ZigZag,Impulse,ZigZag,Impulse)
    def report(self):
        # print primary C 
        print_title(fg.RED,'primary-wave {name}'.format(name=self.name))
        overview(self)
        print_fibs(self)
    #   print_fibs_interwaves()
        print_predictions(self)
        # print intermediate wave i,ii,iii,...
        for subwave in self.subwaves:
            print_title(fg.BLUE,'intermediate {name} Analysis'.format(name=subwave.name))
            overview(subwave)
            if subwave.No in [2,4]: continue
            print_fibs(subwave)
            print_predictions(subwave)

class Intermediate_i(Impulse):
    def __init__(self):
        super(self.__class__,self).__init__(start=14198, end=11730, level=-1, No=1)
        self.create_minors()
        self.creates_minutes_for_minor_i()
    def create_minors(self):
        self.create_subwaves(14198,12724,13778,12069,12756,11731,Impulse,ZigZag,Impulse,ZigZag,Impulse)
        #self.create_subwaves(14198,12724,13778,11640,12756,11731,Impulse,ZigZag,Impulse,ZigZag,Impulse)
    def creates_minutes_for_minor_i(self):
        # minor <i>   : 14198,13408,13962,12975,13367,12724
        # minor <ii>  : 12724,13466,13273,13377              -> ZigZag
        # minor <iii> : 13377,13092,13562,11640,12767,12069  -> 1=5,3
        # minor <iv>  : 12069,12572,12155,12756              -> Flat
        # minor <iii> : 13377,13092,12502,12390,12930,11640  -> 1,3=5
        # minor <iv>  : 11640,12767,12069,12756              -> Unidentified
        # minor <v>   : 12756,12032,12349,None,None,11732    -> Unidentified, 1st wave may be extended
        self.i.create_subwaves(14198,13408,13962,12975,13367,12724,Impulse,ZigZag,Impulse,ZigZag,Impulse)
        self.ii.create_subwaves(12724,13466,13273,13377,Impulse,ZigZag,Impulse)
        self.iii.create_subwaves(13377,13092,13562,11640,12767,12069,Impulse,ZigZag,Impulse,ZigZag,Impulse)
        self.iv.create_subwaves(12069,12572,12155,12756,ZigZag,ZigZag,Impulse)
        #self.iii.create_subwaves(13377,13092,13562,12502,12930,11640,Impulse,ZigZag,Impulse,ZigZag,Impulse)
        #self.iv.create_subwaves(11640,12767,12069,12756,ZigZag,ZigZag,Impulse)
        self.v.create_subwaves(12756,12032,12349,None,None,11731,Impulse,ZigZag,Impulse,ZigZag,Impulse)
    def report(self):
        # print primary C 
        print_title(fg.RED,'intermediate-wave {name}'.format(name=self.name))
        overview(self)
        print_fibs(self)
    #   print_fibs_interwaves()
        print_predictions(self)
        # print intermediate wave i,ii,iii,...
        for subwave in self.subwaves:
            print_title(fg.BLUE,'minor {name} Analysis'.format(name=subwave.name))
            overview(subwave)
            if subwave.No in [2,4]: continue
            print_fibs(subwave)
            print_predictions(subwave)


#   print fg.RED +'superwave [V] Analysis : I,II,III,IV,V\n'

if __name__ == '__main__':
    Intermediate_i().report()
#   PrimaryC().report()

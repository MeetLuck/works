# Primary Wave C of [IV] #
#   start    wave I    wave II   wave III   wave IV    wave V
#   14198    11730     13139     7450       9088       6450  

import sys
sys.path.append('../elliot')

from elliot60 import *

def primaryC():
    def create_intermediates(primary):
        primary.create_subwaves(14198,11730,13139,7450,9088,6450,Impulse,ZigZag,Impulse,ZigZag,Impulse)
    def create_minors(primary):
        # wave i   : 14198,12724,13778,12069,12756,11731
        # wave ii : 11732,12621,12269,13136 -> ZigZag
        # wave iii : 13139,10827,11874,8130,9654,7450 
        # wave iv : 7450,8828,8118,8961,8364,9087 ->Triangle
        # wave v : 9087,7909,8314,7106,7404,6470 
        primary.i.create_subwaves(14198,12724,13778,12069,12756,11731,Impulse,ZigZag,Impulse,ZigZag,Impulse)
        primary.ii.create_subwaves(11732,12621,12269,13136,Impulse,ZigZag,Impulse)
        primary.iii.create_subwaves(13139,10827,11874,8130,9654,7450,Impulse,Flat,Impulse,ZigZag,Impulse)
        primary.iv.create_subwaves(7450,9026,8364,9087,ZigZag,ZigZag,Impulse)
        primary.v.create_subwaves(14198,12724,13778,12069,12756,11731,Impulse,ZigZag,Impulse,ZigZag,Impulse)

#   print fg.RED +'superwave [V] Analysis : I,II,III,IV,V\n'
    primaryC = Impulse(start=14198, end=6450, level=0, No=8)
#   primaryC.create_subwaves(14198,11730,13139,7450,9088,6450,Impulse,ZigZag,Impulse,ZigZag,Impulse)
    create_intermediate(primaryC)
    create_minors(primaryC)
    # print primary C 
    print_title(fg.RED,'primary-wave {name}'.format(name=primaryC.name))
    overview(primaryC)
    print_fibs(primaryC)
#   print_fibs_interwaves()
    print_predictions(primaryC)
    # print intermediate wave i,ii,iii,...
    for subwave in primaryC.subwaves:
        print_title(fg.BLUE,'intermediate {name} Analysis'.format(name=subwave.name))
        overview(subwave)
        if subwave.No in [2,4]: continue
        print_fibs(subwave)
        print_predictions(subwave)

def intermediate_i():
    def create_subwaves(wave):
        # wave <i>  : 14198,12724,13778,12069,12756,11731
        # wave <ii> : 11732,12621,12269,13136 -> ZigZag
        # wave <iii> : 13139,10827,11874,8130,9654,7450 
        # wave <iv>: 7450,8828,8118,8961,8364,9087 ->Triangle
        # wave <v> : 9087,7909,8314,7106,7404,6470 
        wave.i.create_subwaves(14198,12724,13778,12069,12756,11731,Impulse,ZigZag,Impulse,ZigZag,Impulse)
        wave.ii.create_subwaves(11732,12621,12269,13136,Impulse,ZigZag,Impulse)
        wave.iii.create_subwaves(13139,10827,11874,8130,9654,7450,Impulse,Flat,Impulse,ZigZag,Impulse)
        wave.iv.create_subwaves(7450,9026,8364,9087,ZigZag,ZigZag,Impulse)
        wave.v.create_subwaves(14198,12724,13778,12069,12756,11731,Impulse,ZigZag,Impulse,ZigZag,Impulse)

if __name__ == '__main__':
    primaryC()

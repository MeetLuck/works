# Dow Analysis #
# ---- whole wave IV(C) -----
# start     wave I   wave II   wave III   wave IV   wave V
#  14198    11730    13139    7450      9088    6450 
# wave I ( I1,I2,I3,I4,I5 )
# wave II ( A,B,C )
# wave III ( III1,III2,III3,III4,III5 )
# wave IV ( A,B,C )
# wave V ( V1,V2,V3,V4,V5 )
import sys
sys.path.append('../elliot')
from  elliot10 import *
from colorama import Fore as fg, Back as bg, Style as stl
import colorama
colorama.init(autoreset= True)

def whole_wave():
    ''' whole wave predict( I, II, III, IV, V)'''
    wave1   = Wave(14198, 11730)
    wave2   = Wave(11730, 13139)
    wave3   = Wave(13139,7450)
    wave4   = Wave(7450,9088 )
    wave5   = Wave(9088,6450 )
    # predict whole wave
    print fg.RED + stl.BRIGHT + 'predict whole wave C(IV)'
    ew1 = EWaves(wave1,wave2,wave3,wave4,wave5)
    print

# predict whole wave
whole_wave()

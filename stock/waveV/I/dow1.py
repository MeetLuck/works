# Dow Analysis #
# ---- whole wave -----
# start     wave I   wave II   wave III   wave IV   wave V
#  6450     12391     10404     18351      15450     211?
# wave I ( I1,I2,I3,I4,I5 )
# wave II ( A,B,C )
# wave III ( III1,III2,III3,III4,III5 )
# wave IV ( A,B,C )
# wave V ( V1,V2,V3,V4,V5 )

import sys
sys.path.append('../elliot')
from elliot10 import *
from colorama import Fore as fg, Back as bg, Style as stl
import colorama
colorama.init(autoreset= True)

def whole_wave():
    ''' whole wave predict( I, II, III, IV, V)'''
    wave1   = Wave(20380, 20630)
    wave2   = Wave(20630, 20505)
    wave3   = Wave(20505,20792)
    ew1 = EWaves(wave1,wave2,wave3)
    print

# predict whole wave
whole_wave()

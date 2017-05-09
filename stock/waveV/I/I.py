# wave I[V]
# start     wave I   wave II   wave III   wave IV   wave V
#  6450     12391     10404     18351      15450     211?
import sys
sys.path.append('../../elliot')
from  elliot11 import *
from colorama import Fore as fg, Back as bg, Style as stl
import colorama
colorama.init(autoreset= True)

def I():
    '''  wave I analysis 
    6450 - 8877(p1) - 8077(p2) - 11258(p3) - 9614(p4) - 12391(p5)
    '''
    wave1   = Wave(6450, 8877)
    wave2   = Wave(8877, 8077)
    wave3   = Wave(8077,11258)
    wave4   = Wave(11258,9614 )
    wave5    = Wave(9614, 12391)
#   wave3    = Wave(8077,10730)
#   wave4    = Wave(10730,9614)
    print fg.RED +'wave I Analysis : I1, I2, I3, I4, I5'
    ew1 = EWaves(wave1,wave2,wave3,wave4,wave5)
    print

I()

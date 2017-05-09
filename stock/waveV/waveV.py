#  wave [V]
# start     wave I   wave II   wave III   wave IV   wave V
#  6450     12391     10404     18351      15450     211?

import sys
sys.path.append('../elliot')
from  elliot11 import *
from colorama import Fore as fg, Back as bg, Style as stl
import colorama
colorama.init(autoreset= True)

def waveV():
    '''  wave [V] analysis 
    6450 - 12391(p1) - 10404(p2) - 18351(p3) - 15450(p4) - ?(p5)
    '''
    wave1   = Wave(6450, 12391)
    wave2   = Wave(12391,10404)
    wave3   = Wave(10404,18351)
    wave4   = Wave(18351,15450)
    # predict whole wave
    print fg.RED + stl.BRIGHT + 'predict whole wave'
    ew1 = EWaves(wave1,wave2,wave3,wave4)
    print

# predict wave [V]
waveV()

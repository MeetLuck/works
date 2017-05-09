# wave I of wave V

import sys
sys.path.append('../../elliot')
from elliot11 import *
from colorama import Fore as fg, Back as bg, Style as stl
import colorama
colorama.init(autoreset= True)

def waveV1():
    ''' I of wave V ''' 
    wave1   = Wave(20380, 20630)
    wave2   = Wave(20630, 20505)
    wave3   = Wave(20505, 20792)
    wave3a  = Wave(20505, 21075)
    ew1 = EWaves(wave1,wave2,wave3)
    ew2 = EWaves(wave1,wave2,wave3a)
    print

# predict whole wave
waveV1()

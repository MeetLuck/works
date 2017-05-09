# Dow Analysis #
# ---- wave III of wave C -----
# start     wave I   wave II   wave III   wave IV   wave V
# 13139    10827    11874        8130      9654    7450 
import sys
sys.path.append('../elliot')
from  elliot10 import *
from colorama import Fore as fg, Back as bg, Style as stl
import colorama
colorama.init(autoreset= True)

def waveIII():
    ''' wave III of wave C ''' 
    wave1   = Wave(13139, 10827)
    wave2   = Wave(10827, 11874)
    wave3   = Wave(11874,8130)
    wave4   = Wave(8130,9654 )
    wave5   = Wave(9654,7450 )
    # predict whole wave
    print fg.RED + stl.BRIGHT + 'wave III(C)'
    ew1 = EWaves(wave1,wave2,wave3,wave4,wave5)
    print

# predict whole wave
waveIII()

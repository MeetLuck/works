# Dow Analysis #
# ---- wave I of wave C -----
# start     wave I   wave II   wave III   wave IV   wave V
# 14198    12724    13780        12069      12756    11731 
import sys
sys.path.append('../elliot')
from  elliot10 import *
from colorama import Fore as fg, Back as bg, Style as stl
import colorama
colorama.init(autoreset= True)

def waveI1():
    ''' wave I of wave C ''' 
    wave1   = Wave(14198,13407)
    wave2   = Wave(13407,13962)
    wave3   = Wave(13962,12975)
    wave4   = Wave(12975,13367)
    wave5   = Wave(13367,12724)
    # predict whole wave
    print fg.RED + stl.BRIGHT + 'wave I1(C)'
    ew1 = EWaves(wave1,wave2,wave3,wave4,wave5)
    print

# predict or analyze wave I1(C)
waveI1()

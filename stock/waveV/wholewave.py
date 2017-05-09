# wave [V]
# start     wave I   wave II   wave III   wave IV   wave V
#  6450     12391     10404     18351      15450     211?
import sys
sys.path.append('../elliot')
from  elliot11 import *
from colorama import Fore as fg, Back as bg, Style as stl
import colorama
colorama.init(autoreset= True)

def V():
    '''  wave [V] analysis 
    6450 - 12391(p1) - 10404(p2) - 18351(p3) - 15450(p4) - ?(p5)
    '''
    wave1   = Wave(6450, 12391)
    wave2   = Wave(12391, 10404)
    wave3   = Wave(10404,18351)
    wave4   = Wave(18351,15450 )
    # predict whole wave
    print fg.RED + stl.BRIGHT + 'predict whole wave'
    ew1 = EWaves(wave1,wave2,wave3,wave4)
    print

def i():
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

def iii():
    '''  wave III analysis 
    10404 - 13662(p1) - 12471(p2) - 17279(p3) - 15885(p4) - 18351(p5)
    '''
    wave1 = Wave(10404,13662)
    wave2 = Wave(13662,12471)
    wave3 = Wave(12471,17279)
    wave4 = Wave(17279,15885)
    wave5 = Wave(15885,18351)
    print
    print fg.RED +'wave III Analysis : III1, III2, III3, III4, III5'
    ew1 = EWaves(wave1,wave2,wave3,wave4,wave5)
    # predict wave 3
    ew2 = EWaves(wave1)
    print

V()
i()
iii()

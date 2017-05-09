#  wave [V]
# start     wave I   wave II   wave III   wave IV   wave V
#  6450     12391     10404     18351      15450     211?

import sys
sys.path.append('../elliot')
from  elliot11 import *
from colorama import Fore as fg, Back as bg, Style as stl
import colorama
colorama.init(autoreset= True)

def whole_wave():
    ''' whole wave predict( I, II, III, IV, V)'''
    wave1   = Wave(6450, 12391)
    wave2   = Wave(12391, 10404)
    wave3   = Wave(10404,18351)
    wave4   = Wave(18351,15450 )
    # predict whole wave
    print fg.RED + stl.BRIGHT + 'predict whole wave'
    ew1 = EWaves(wave1,wave2,wave3,wave4)
    print

def waveI():
    ''' wave I Analysis( I1,I2,I3,I4,I5) '''
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

def waveIII():
    ''' wave III Analysis( III1,III2,III3,III4,III5) '''
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

def waveV(): 
    ''' wave V Analysis ( V1, V2, V3, V4, V5) '''
    wave1 = Wave(15450,18167)
    wave2 = Wave(18167,17140)
    wave3 = Wave(17140,21170)
    # predict wave 3
    print
    print fg.RED +'predict wave V'
    ew1 = EWaves(wave1,wave2,wave3)
    print

def waveV3():
    '''  wave V.3 analysis 
    17063 - 18668(p1) - 17884(p2) - 19909(p3) - 19668(p4) - 21170(p5)
    '''
    wave1 = Wave(17063,18668)
    wave2 = Wave(18668,17884)
    wave3 = Wave(17884,19909)
    wave4 = Wave(19909,19668)
    wave5 = Wave(19668,21170)
    print
    print fg.RED +'analyze wave V.3'
    ew = EWaves(wave1,wave2,wave3,wave4,wave5)

# predict whole wave
whole_wave()
# analyze wave I
waveI()
# analyze wave III
waveIII()
# predict wave V
waveV()
# analyze wave V.3
waveV3()

#  wave III of [V]
# start     wave I   wave II   wave III   wave IV   wave V
#  10404    13662     12471     17279     15885     18351
#  10404    13300     12035     16588     15353     18351

import sys
sys.path.append('../../elliot')
from  elliot11 import *
from colorama import Fore as fg, Back as bg, Style as stl
import colorama
colorama.init(autoreset= True)

def III_x():
    ''' wave III Analysis
    10404 - 13662(p1) - 12471(p2) - 17279(p3) - 15885p4) - 18351(p5)
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
    # ew2 = EWaves(wave1)
    print

def III_y():
    ''' wave III Analysis
    10404 - 13300(p1) - 12035(p2) - 16588(p3) - 15355(p4) - 18351(p5)
    '''
    wave1 = Wave(10404,13300)
    wave2 = Wave(13300,12035)
    wave3 = Wave(12035,16588)
    wave4 = Wave(16588,15335)
    wave5 = Wave(15335,18351)
    print
    print fg.RED +'wave III Analysis : III1, III2, III3, III4, III5'
    ew1 = EWaves(wave1,wave2,wave3,wave4,wave5)
    print

# analyze wave III
III_x()
III_y()

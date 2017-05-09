# wave V of [V]
# start     i       ii      iii     iv      v
# 15450     18167   17140   21170   ???     
import sys
sys.path.append('../../elliot')
from  elliot11 import *

def V():
    '''  wave V analysis 
    15450 - 18167(p1) - 17140(p2) - 21170(p3) - ?(p4) - ?(p5)
    a = 2717, b = -1027, c = 4030, d = , e = -780
    '''
    wave1 = Wave(15450,18167)
    wave2 = Wave(18167,17140)
    wave3 = Wave(17140,21170)
    print
    print fg.RED +'predict wave V'
    ew1 = EWaves(wave1,wave2,wave3)
    print

def iii():
    '''  wave iii analysis 
    17063 - 18668(p1) - 17884(p2) - 19909(p3) - 19668(p4) - 21170(p5)
    a = 1605, b = -784, c = 2025, d = -241, e = 1502
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
V()
# analyze wave V.3
iii()

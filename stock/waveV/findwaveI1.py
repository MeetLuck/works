# find wave I.1 of wave C(I,II,...)
# start     wave C
#  21075    19677

import sys
sys.path.append('../elliot')
from elliot10 import *
from colorama import Fore as fg, Back as bg, Style as stl
import colorama
colorama.init(autoreset= True)

def waveI1():
    p0,p5 = 21075,19677
    waveC   = Wave(p0,p5)
    a = waveC.size/2.382
    p1 = p0 + a
    print 'wave C'
    print 'size(C): {size}'.format(size = waveC.size) 
    print 'p1(a) : {p1:9}({a})'.format(p1=int(p1),a=int(a))
    print 'wave I.1'
    waveI = Wave(p0,p1)
    a1 = waveI.size/2.382
    p1 = p0 + a1
    print 'size(I): {size}'.format(size = int(waveI.size) )
    print 'p1(a) : {p1:9}({a})'.format(p1=int(p1),a=int(a1))

# predict whole wave
waveI1()

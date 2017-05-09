# Elliot Wave Analysis [V] #
#   start       wave I         wave II         wave III        wave IV         wave V
# 6450(0) -> 12391(+5951) -> 10404(-1987) -> 18351(+7906) -> 15450(-2906) -> 20401?(+5941?)

# super waves(level +1)         :  [I]  [II]  [III]  [IV]  [V]   ...  [A] [B] [C] (about decade(10 years) )
# primary waves(level 0)        :   I    II    III    IV    V    ...  A B C for [II], [IV](about serveral years)
# intermediate waves(level -1)  :   i    ii    iii    iv    v    ...  a b c for II, IV (about serveral months)

import colorama,sys
from string import Template
from colorama import Fore as fg, Back as bg, Style as stl
colorama.init(autoreset=True)
sys.path.append('../elliot')

from elliot20 import *

class superV:
    def __init__(self):
        self.super_V = Motive(start=6450,end=None,level=+1,no=5)
        self.set_super_V()
        self.set_primary_I()
        self.set_primary_II()
        self.set_primary_III()
        self.set_primary_IV()
        self.set_primary_V()
    def set_super_V(self):
        self.I   = Motive(start=6450, end=12391, level=0, no=1)
        self.II  = Motive(start=12391,end=10404, level=0, no=2)
        self.III = Motive(start=10404,end=18351, level=0, no=3)
        self.IV  = Motive(start=18351,end=15450, level=0, no=4)
        self.V   = Motive(start=15450,end=None,  level=0, no=5)
        self.super_V.set_subwaves(self.I,self.II,self.III,self.IV,self.V)
#       self.superV.report_all()
    def set_primary_I(self):
        '''  wave I : 6450 - 8877(p1) - 8077(p2) - 11258(p3) - 9614(p4) - 12391(p5)
        '''
        i    = Motive(start=6450,  end=8877,  level=-1, no=1)
        ii   = Motive(start=8877,  end=8077,  level=-1, no=2)
        iii  = Motive(start=8077,  end=11258, level=-1, no=3)
        iv   = Motive(start=11258, end=9614,  level=-1, no=4)
        v    = Motive(start=9614,  end=12391, level=-1, no=5)
        #   wave3    = Wave(8077,10730)
        #   wave4    = Wave(10730,9614)
        self.I.set_subwaves(i,ii,iii,iv,v)
    def set_primary_II(self):
        '''  wave II : 12391 - 11556(a) - 12876(b)  - 10404(c)
                       irregular correction(3-3-5)
        '''
        a    = Corrective(start=12391,  end=11556,  level=-1, no=6)
        b    = Corrective(start=11556,  end=12876,  level=-1, no=7)
        c    = Corrective(start=12876,  end=10404,  level=-1, no=8)
        self.II.set_subwaves(a,b,c)
    def set_primary_III(self):
        '''  wave III : 10404 - 13662(p1) - 12471(p2) - 17279(p3) - 15885(p4) - 18351(p5)
                        10404 - 13300(p1) - 12035(p2) - 16588(p3) - 15355(p4) - 18351(p5)
        '''
        i    = Motive(start=10404,  end=13662,  level=-1, no=1)
        ii   = Motive(start=13662,  end=12471,  level=-1, no=2)
        iii  = Motive(start=12471,  end=17279,  level=-1, no=3)
        iv   = Motive(start=17279,  end=15885,  level=-1, no=4)
        v    = Motive(start=15885,  end=18351,  level=-1, no=5)
        self.III.set_subwaves(i,ii,iii,iv,v)
    def set_primary_IV(self):
        '''  wave IV : 18351 - 15370(a) - 17987(b)  - 15450(c)'''
        a    = Corrective(start=18351,  end=15370,  level=-1, no=6)
        b    = Corrective(start=15370,  end=17987,  level=-1, no=7)
        c    = Corrective(start=17987,  end=15450,  level=-1, no=8)
        self.II.set_subwaves(a,b,c)

    def set_primary_V(self):
        '''  wave V : 15450 - 18167(p1) - 17140(p2) - 21170(p3) - 20375(p4) - ?(p5) '''
        i    = Motive(start=15450,  end=18167,  level=-1, no=1)
        ii   = Motive(start=18167,  end=17140,  level=-1, no=2)
        iii  = Motive(start=17140,  end=21170,  level=-1, no=3)
        iv   = Motive(start=21170,  end=20375,  level=-1, no=4)
        v    = Motive(start=20375,  end=None,   level=-1, no=5)
        self.V.set_subwaves(i,ii,iii,iv,v)
    def analyze(self):
        if not self.super_V.has_subwave: return
        s1 = self.I.size
        s2 = self.II.size
        s3 = self.III.size
        s4 = self.IV.size
        s5 = None
        s31 = s3/s1 # fib 0.62
        s21 = s2/s1 # fib 1.0
        s43 = s4/s3 # fib 0.38
        s51 = None
        print
        print 'analyzing superwave [V]...'
        print 'wave3/wave1:{s31:5.2f},wave2/wave1:{s21:5.2f}, wave4/wave3:{s43:5.2f}'.format(s31=s31,s21=s21,s43=s43)


print fg.RED +'superwave [V] Analysis : I,II,III,IV,V'
superwaveV = superV()
superwaveV.super_V.report_all()
superwaveV.analyze()

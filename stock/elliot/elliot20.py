# Elliot Wave Analysis [V] #
#   start       wave I         wave II         wave III        wave IV         wave V
# 6450(0) -> 12391(+5951) -> 10404(-1987) -> 18351(+7906) -> 15450(-2906) -> 20401?(+5941?)

# super waves(level +1)         :  [I]  [II]  [III]  [IV]  [V]   ...  [A] [B] [C] (about decade(10 years) )
# primary waves(level 0)        :   I    II    III    IV    V    ...  A B C for [II], [IV](about serveral years)
# intermediate waves(level -1)  :   i    ii    iii    iv    v    ...  a b c for II, IV (about serveral months)

import colorama
from string import Template
from colorama import Fore as fg, Back as bg, Style as stl
colorama.init(autoreset=True)

class Wave:
    def __init__(self,start,end=None,level=None,no=None):
        '''
        level -1 for intermediate, level 0 for primary, level 1 for super  
        no 1,2,3,4,5 for motive, no 6,7,8 for corrective
        '''
        self.level = level
        self.no = no
        self.has_subwave = False
        self.subwaves = None
        self.size = None
        self.set_name()
        self.start = float(start)
        if end is None:
            self.end = end # None
            self.complete = False
        else:
            self.end = float(end)
            self.complete = True
            self.compute_size()
    def set_name(self):
        if self.level == +1:
            if   self.no == 1: self.name = '[I]'
            elif self.no == 2: self.name = '[II]'
            elif self.no == 3: self.name = '[III]'
            elif self.no == 4: self.name = '[IV]'
            elif self.no == 5: self.name = '[V]'
        elif self.level == 0:
            if   self.no == 1: self.name = 'I'
            elif self.no == 2: self.name = 'II'
            elif self.no == 3: self.name = 'III'
            elif self.no == 4: self.name = 'IV'
            elif self.no == 5: self.name = 'V'
        elif self.level == -1:
            if   self.no == 1: self.name = 'i'
            elif self.no == 2: self.name = 'ii'
            elif self.no == 3: self.name = 'iii'
            elif self.no == 4: self.name = 'iv'
            elif self.no == 5: self.name = 'v'

    def compute_size(self):
        self.size = self.end - self.start
        self.percent = 100.0*self.size/self.start
    def report(self):
        print '{name:^7}:  {start:7} - {end:7}\t {size:7}'.format(name=self.name,start=self.start,end=self.end, size = self.size)

class Motive(Wave):
    def __init__(self,start,end=None,level=None,no=None):
        '''
            motives wave -> 1,2,3,4,5
            intermediate (i,ii,...,v) -> primary (I,II,..,V) -> super [I],[II],[III],[IV],[V]
        '''
        # super(Motive,self).__init__(start,end,level,no)
        Wave.__init__(self,start,end,level,no)

    def set_subwaves(self, *waves):
        if self.level == -1 :
            raise Exception('waves must greather than intermediate')
        if self.no in [1,3,5]:
            self.set_motives(*waves)
            self.subwaves = self.i, self.ii, self.iii,self.iv,self.v
            self.has_subwave = True
        elif self.no in [2,4]:
            self.set_correctives(*waves)
            self.subwaves = self.a, self.b, self.c
            self.has_subwave = True
        else:
            raise Exception('number of waves not valid')

    def report_all(self):
        self.report()
        if self.has_subwave:
            for sub in self.subwaves: sub.report()

    def set_motives(self,*waves):
        # set motive waves(1-2-3-4-5)
        if len(waves) >= 1: self.i    = waves[0]
        if len(waves) >= 2: self.ii   = waves[1]
        if len(waves) >= 3: self.iii  = waves[2]
        if len(waves) >= 4: self.iv   = waves[3]
        if len(waves) >= 5: self.v    = waves[4]

    def set_correctives(self, *waves):
        # set corrective waves(a-b-c)
        self.a = waves[0]
        self.b = waves[1]
        self.c = waves[2]


class Corrective(Wave):
    def __init__(self,start,end=None,level=None,no=None):
        '''
            corrective waves -> a,b,c
            intermediate (a,b,c) -> primary (A,B,C) -> super [A],[B],[C]
        '''
        # super(Motive,self).__init__(start,end,level,no)
        Wave.__init__(self,start,end,level,no)

if __name__ == '__main__':
    superV = Motive(start=6450,end=None,level=+1,no=5)
    I   = Motive(start=6450, end=12391, level=0, no=1)
    II  = Motive(start=12391,end=10404, level=0, no=2)
    III = Motive(start=10404,end=18351, level=0, no=3)
    IV  = Motive(start=18351,end=15450, level=0, no=4)
    V   = Motive(start=15450,end=None,  level=0, no=5)
    superV.set_subwaves(I,II,III,IV,V)
    superV.report_all()

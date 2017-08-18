# Elliot Wave Analysis [V] #
#   start       wave I         wave II         wave III        wave IV         wave V
# 6450(0) -> 12391(+5951) -> 10404(-1987) -> 18351(+7906) -> 15450(-2906) -> 20401?(+5941?)

# super waves(level +1)         :  [I]  [II]  [III]  [IV]  [V]   ...  [A] [B] [C] (about decade(10 years) )
# primary waves(level 0)        :   I    II    III    IV    V    ...  A B C for [II], [IV](about serveral years)
# intermediate waves(level -1)  :   i    ii    iii    iv    v    ...  a b c for II, IV (about serveral months)

import colorama
from colorama import Fore as fg, Back as bg, Style as stl
colorama.init(autoreset=True)

class Wave:
    def __init__(self,start,end=None,level=None,no=None):
        '''
        level -1 for intermediate, level 0 for primary, level 1 for super  
        no 1,2,3,4,5 for motive, no 6,7,8 for corrective
        '''
        self.level        = level
        self.no           = no
        self.subwaves     = None
        self.has_subwaves = False
        self.size         = None
        self.set_name()
        self.start = float(start)
        if end is None:
            self.end = end # None
            self.complete = False
        else:
            self.end = float(end)
            self.complete = True
            self.compute_size()
            self.compute_percent()
    def set_name(self):
        Literal = 'unused','I','II','III','IV','V','A','B','C'
        if self.level  == +1:  # [I] [II] ....[A] [B] [C]
            self.name = '[' + Literal[self.no]+ ']'
        elif self.level == 0: # I  II .... A B C
            self.name = Literal[self.no] 
        elif self.level == -1: # i ii .... a b c
            self.name = Literal[self.no].lower() 
        else:
            self.name = None

    def compute_size(self):
        self.size = self.end - self.start
    def compute_percent(self):
        self.percent = 100.0*self.size/self.start
    def __str__(self):
        return '    {name:5} :  {start:8} - {end:<9}\t {size:<7}'.format(name=self.name,start=self.start,end=self.end, size = self.size)

class Motive(Wave):
    def __init__(self,start,end=None,level=None,no=None):
        '''
            motives wave -> 1,2,3,4,5
            intermediate (i,ii,...,v) -> primary (I,II,..,V) -> super [I],[II],[III],[IV],[V]
        '''
        # super(Motive,self).__init__(start,end,level,no)
        Wave.__init__(self,start,end,level,no)

    def report(self):
        print str(self)
        print fg.GREEN + '-'*70
        if self.has_subwaves:
            for subwave in self.subwaves: print subwave

    def set_motives(self,start=None,p1=None,p2=None,p3=None,p4=None,p5=None):
        # set motive waves(1-2-3-4-5)
        assert self.no in [1,3,5], 'motive waves required, not correctives'
        self.has_subwaves = True
        self.i   = Motive(start=start,end=p1,level=self.level-1,no=1)
        self.ii  = Motive(start=p1,   end=p2,level=self.level-1,no=2)
        self.iii = Motive(start=p2,   end=p3,level=self.level-1,no=3)
        self.iv  = Motive(start=p3,   end=p4,level=self.level-1,no=4)
        self.v   = Motive(start=p4,   end=p5,level=self.level-1,no=5)
        self.subwaves = self.i, self.ii, self.iii, self.iv, self.v

    def set_correctives(self, start = None, pa=None, pb=None,pc=None):
        # set corrective waves(a-b-c)
        assert self.no in [2,4],'corrective waves required, not motives'
        level = self.level - 1
        self.has_subwaves = True
        self.a = Corrective(start=start,end=pa,level=level,no=6)
        self.b = Corrective(start=pa,   end=pb,level=level,no=7)
        self.c = Corrective(start=pb,   end=pc,level=level,no=8)
        self.subwaves = self.a, self.b, self.c
    def fib(self,sub_y,sub_x):
        ''' e.g. fib(2,1) -> sub-wave 2/sub-wave 1 for wave 1,3,5
            e.g. fib(2,1) -> sub-wave b/sub-wave a for wave 2, 4'''
        if self.subwaves[sub_y-1].complete:
            return self.subwaves[sub_y-1].size/self.subwaves[sub_x-1].size
    def fib20(self):
        return (self.iii.end - self.start)/self.i.size
    def fib238(self):
        return self.size/self.i.size
    def fib_sub_31to11(self):
        return self.iii.i.size/self.i.i.size
    def fib_sub_33to13(self):
        return self.iii.iii.size/self.i.iii.size
    def fib_sub_35to15(self):
        return self.iii.v.size/self.i.v.size
    def fib_sub20(self):
        return (self.i.iii.end - self.start)/self.i.i.size
    def fib_sub238(self):
        return (self.i.v.end - self.start)/self.i.i.size
    def fib_sub253(self):
        return (self.iii.i.end - self.start)/self.i.i.size
    def fib_sub414(self):
        return (self.iii.iii.end - self.start)/self.i.i.size
    def fib_sub476(self):
        return (self.iii.v.end - self.start)/self.i.i.size
    def predict_wave5from4(self):
        return self.iv.end + 1.0*self.i.size
    def predict_wave5from3(self):
        return self.iii.end + 0.382*self.i.size


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
    superV.set_motives(start=6450,p1=12391,p2=10404,p3=18351,p4=15450,p5=None)
    superV.report()

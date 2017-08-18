# Elliot Wave 

import colorama
from colorama import Fore as fg, Back as bg, Style as stl
colorama.init(autoreset=True)

class Wave:
    def __init__(self,start,end=None,level=None,no=None):
        '''
        INTERMEDIATE (i,ii,...,v) -> PRIMARY (I,II,..,V) -> SUPER [I],[II],[III],[IV],[V]
        level -1 for intermediate, level 0 for primary, level 1 for super wave  
        no 1,2,3,4,5 for motive, no 6,7,8 for corrective wave
        '''
        self.level        = level
        self.no           = no
        self.start        = start
        self.end          = end
        self.subwaves     = None
        self.has_subwaves = False
        self.complete     = False
        self.size         = None
        self.set_name()
        if self.start is not None:
            self.start    = float(start)
        if self.end is not None:
            # compute size, percent
            self.complete = True
            self.end      = float(end)
            self.size     = self.end - self.start
            self.percent  = 100.0*self.size/self.start

    def set_motives(self,start,p1=None,p2=None,p3=None,p4=None,p5=None):
        # set motive waves(1-2-3-4-5) for I,III,V
        assert self.no in [1,3,5], 'motive waves required, not correctives'
        self.has_subwaves = True
        self.i = Motive(start=start, end=p1, level=self.level-1, no=1)
        self.ii  = Motive(start=p1, end=p2, level=self.level-1, no=2)
        self.iii = Motive(start=p2, end=p3, level=self.level-1, no=3)
        self.iv  = Motive(start=p3, end=p4, level=self.level-1, no=4)
        self.v   = Motive(start=p4, end=p5, level=self.level-1, no=5)
        self.subwaves = self.i, self.ii, self.iii, self.iv, self.v

    def set_correctives(self, start, pa=None, pb=None,pc=None):
        # set corrective waves(a-b-c) for II,IV
        assert self.no in [2,4],'corrective waves required, not motives'
        level = self.level - 1
        self.has_subwaves = True
        self.a = Corrective(start=start,end=pa,level=level,no=6)
        self.b = Corrective(start=pa,   end=pb,level=level,no=7)
        self.c = Corrective(start=pb,   end=pc,level=level,no=8)
        self.subwaves = self.a, self.b, self.c

    def set_name(self):
        Literal = 'unused','I','II','III','IV','V','A','B','C'
        if self.level  == +1:  # [I] [II] ....[A] [B] [C]
            self.name = '[' + Literal[self.no]+ ']'
        elif self.level == 0: # I  II .... A B C
            self.name = Literal[self.no] 
        elif self.level == -1: # i ii .... a b c
            self.name = Literal[self.no].lower() 
        elif self.level == -2: # <i> <ii>  .... <a> <b> <c>
            self.name = '<'+Literal[self.no].lower()+'>'
        else:
            self.name = 'Unidentified'

    def __str__(self):
        return '    {name:5} :  {start:8} - {end:<9}\t {size:<7}'.format(name=self.name,start=self.start,end=self.end, size = self.size)

class Motive(Wave):
    def __init__(self,start,end=None,level=None,no=None):
        '''
            MOTIVES wave -> 1,2,3,4,5
        '''
        # super(Motive,self).__init__(start,end,level,no)
        Wave.__init__(self,start,end,level,no)

    def fib(self,sub_y,sub_x):
        ''' e.g. fib(2,1) -> sub-wave 2/sub-wave 1 for wave 1,3,5 '''
        subwave_y,subwave_x = self.subwaves[sub_y-1], self.subwaves[sub_x-1]
        assert subwave_y.complete,'wave {name} NOT completed'.format(name = subwave_y.name)
        return subwave_y.size/subwave_x.size

    def fib20(self):
        assert self.iii.complete,'wave {name} NOT completed'.format(name=self.iii.name)
        return (self.iii.end - self.i.start)/self.i.size

    def fib238(self):
        assert self.v.complete,'wave {name} NOT completed'.format(name=self.v.name)
        return (self.v.end - self.i.start)/self.i.size

    def fib_interwaves(self,sub_y,sub_x,waveNo): # subwave_y[wave No]/subwave_x[wave No]
        subwave_y, subwave_x = self.subwaves[sub_y-1], self.subwaves[sub_x-1]
        return subwave_y.subwaves[waveNo-1].size/subwave_x.subwaves[waveNo-1].size

    def fib_wave35from12(self):
        return (self.v.end - self.iii.end)/(self.ii.end - self.i.start)

    def predict_wave3(self,fib_ratio=2.0):                    # wave3 = 2.0 * wave1
        return self.i.start + fib_ratio * self.i.size

    def predict_wave5from1(self,fib_ratio=2.382):             # wave5 = 2.382 * wave1
        return self.i.start + fib_ratio * self.i.size

    def predict_wave5from2(self):                             # wave5 = wave3 + (p2-p1)
        if self.iii.complete:
            p3 = self.iii.end
        else:
            p3 =  self.predict_wave3()
        return p3 + (self.ii.end - self.i.start) 

    def predict_wave5from3(self,fib_ratio=0.382):             # wave5 = wave3 + 0.382 * wave1
        if self.iii.complete:
            p3 = self.iii.end
        else:
            p3 =  self.predict_wave3()
        return p3 + fib_ratio * self.i.size

    def predict_wave5from4(self,fib_ratio=1.0):               # wave5 = 1.0 * wave1
        return self.iv.end + fib_ratio * self.i.size

    def report(self):
        print str(self)
        print fg.WHITE + '-'*70
        if self.has_subwaves:
            for subwave in self.subwaves: print subwave


class Corrective(Wave):
    def __init__(self,start,end=None,level=None,no=None):
        '''
            corrective waves -> a,b,c
            intermediate (a,b,c) -> primary (A,B,C) -> super [A],[B],[C]
        '''
        # super(Motive,self).__init__(start,end,level,no)
        Wave.__init__(self,start,end,level,no)

def print_data(title, data):
    print '    {title} : {data:5.2f}'.format(title=title,data=data)
def print_title(color,title):
    print color + '\n{:^60}\n'.format(title)
def print_subtitle(color,title,name):
    print color + '\n{title} {name}'.format(title=title,name=name)

if __name__ == '__main__':
    superV = Motive(start=6450,end=None,level=+1,no=5)
    superV.set_motives(start=6450,p1=12391,p2=10404,p3=18351,p4=15450,p5=None)
    superV.report()

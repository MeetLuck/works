' WAVE DEGREE '
# Cycle(hundreds)            :  {I} {II} {III} {IV} {V},   {A} {B} {C}
# Grand(decades)             :  [I} [II] [III] [IV] [V],   [A} [B] [C]
# Super(years)               :  (I) (II) (III) (IV) (V),   (A) (B) (C)
# ---------------------------------------------------------------------
# Primary(months)            :  I    II   III   IV   V,     A   B   C
# Intermediate(days)         :  i    ii   iii   iv   v,     a   b   c
# Minor(hours)               : (i)  (ii)  (iii) (iv) (v),  (a) (b) (c)
# Minute(minutes)            : <i>  <ii>  <iii> <iv> <v>,  <a> <b> <c>

import sys
sys.path.append('../elliot')

from helper import *
from toXls import * 

class Wave(object):

    def __new__(cls,*args,**kwargs):
        if cls.__name__ in ('Wave','Motive','Corrective'):
            raise TypeError('cannot instantiate directly')
        return object.__new__(cls,*args,**kwargs)

    def __init__(self,start,end,level,No,has_subwaves=False):
        self.start, self.end, self.level, self.No = start,end,level,No
        self.has_subwaves = has_subwaves
        self.subwaves = None
        self.name  = set_name(level,No)
        self.name2 = set_name2(level,No)
        self.percent = compute_percent(start,end)
        try:
            self.size = float(end) - float(start)
        except: 
            self.size = None

    def __str__(self):
        return '    {name:5} :  {start:8} - {end:<9} {size:>6} {percent:>9}'\
               .format(name=self.name,start=self.start,end=self.end, size = self.size, percent=self.percent)

    def analyze(self):
        self._analyze()
        print '\n'*4
        if self.has_subwaves:
            for subwave in self.subwaves:
                subwave._analyze()

    def _analyze(self, depth=[0]):
        print_title(fg.RED,self.name2)
        overview(self)
        if isinstance(self,Impulse):
            print_fibs(self)
            #print_fibs_interwaves(self)
            print_predictions(self)
        if depth[0] >= 1: return 
        if not self.has_subwaves: return
        for subwave in self.subwaves:
            depth[0] += 1
            subwave.analyze()
            depth[0] -= 1

    def create_xls(self,workbook,filename):
        sheet = WaveToXls(workbook,self)
        self.create(sheet)
        if self.has_subwaves:
            for subwave in self.subwaves:
                sheet = WaveToXls(workbook,subwave)
                subwave.create(sheet)
        workbook.save(filename)

    def create(self,sheet,depth=[0]):
        sheet.overview(self)
        if isinstance(self,Impulse):
            sheet.nextline()
            sheet.fibs(self)
            sheet.nextline()
            sheet.predict(self)
            sheet.nextline()
        if depth[0] >= 1: return 
        if not self.has_subwaves: return
        sheet.nextline(no=2)
        for subwave in self.subwaves:
            depth[0] += 1
            subwave.create(sheet)
            depth[0] -= 1
            sheet.nextline()

class Motive(Wave):

    def create_subwaves(self,p0,p1,p2,p3,p4,p5,wave1,wave2,wave3,wave4,wave5):
        self.prices = p0,p1,p2,p3,p4,p5
        self.i   = wave1(start=p0,end=p1,level=self.level-1, No=1)
        self.ii  = wave2(start=p1,end=p2,level=self.level-1, No=2)
        self.iii = wave3(start=p2,end=p3,level=self.level-1, No=3)
        self.iv  = wave4(start=p3,end=p4,level=self.level-1, No=4)
        self.v   = wave5(start=p4,end=p5,level=self.level-1, No=5)
        self.subwaves = self.i, self.ii, self.iii, self.iv, self.v

    def set_subwaves(self,*waves):
        assert self.has_subwaves,'{wave} has NO subwaves'.format(wave=self)
        assert len(waves)==5,'Motive consists of five waves'
        self.i,self.ii,self.iii,self.iv,self.v =  waves
        self.subwaves = self.i, self.ii, self.iii, self.iv, self.v

    def fib(self,sub_y,sub_x):
        ''' e.g. fib(2,1) -> sub-wave 2/sub-wave 1 for wave 1,3,5 '''
        try:
            subwave_y,subwave_x = self.subwaves[sub_y-1], self.subwaves[sub_x-1]
            return subwave_y.size/subwave_x.size
        except TypeError: return 0

    def fib20(self):
        try: return (self.iii.end - self.i.start)/self.i.size
        except TypeError: return 0

    def fib238(self):
        try: return (self.v.end - self.i.start)/self.i.size
        except TypeError: return 0

    def fibs_interwaves(self,sub_y,yNo,sub_x,xNo): # subwave_y[wave No]/subwave_x[wave No]
        subwave_y, subwave_x = self.subwaves[sub_y-1], self.subwaves[sub_x-1]
        try: return subwave_y.subwaves[yNo-1].size/subwave_x.subwaves[xNo-1].size
        except TypeError: return 0

    def fib_wave35from12(self): # (p5-p3)/(p2-p1)
        try: return (self.v.end - self.iii.end)/(self.ii.end - self.i.start)
        except TypeError: return 0


class Corrective(Wave): # ZigZag, Flat, Double ZigZag

    def create_subwaves(self,p0,pa,pb,pc,wave_a,wave_b,wave_c):
        ''' set default wave type = ZigZag(5-3-5) '''
        self.prices = p0,pa,pb,pc
        self.a  = wave_a(start=p0,end=pa,level=self.level-1, No=6)
        self.b  = wave_b(start=pa,end=pb,level=self.level-1, No=7)
        self.c  = wave_c(start=pb,end=pc,level=self.level-1, No=8)
        self.subwaves = self.a, self.b, self.c

    def set_subwaves(self,*waves):
        assert self.has_subwaves,'{wave} has NO subwaves'.format(wave=self)
        assert len(waves)==3,'Corrective waves consists of three waves'
        for wave in waves:
            assert wave.No >=6,'wave No must be one of 6,7,8 for corrective'
        self.subwaves = self.a,self.b,self.c =  waves


class Impulse(Motive):

    def predict_wave3(self,fib_ratio=2.0):                    # wave3 = 2.0 * wave1
        try: return self.i.start + fib_ratio * self.i.size
        except TypeError: return 0

    def predict_wave5from1(self,fib_ratio=2.382):             # wave5 = 2.382 * wave1
        try: return self.i.start + fib_ratio * self.i.size
        except TypeError: return 0

    def predict_wave5from2(self):                             # wave5 = wave3 + (p2-p1)
        try: # if subwave 3 is completed
            return self.iii.end + (self.ii.end - self.i.start) 
        except TypeError:
            try: # predict p3 first
                return self.predict_wave3() + (self.ii.end - self.i.start) 
            except:
                return 0

    def predict_wave5from3(self,fib_ratio=0.382):             # wave5 = wave3 + 0.382 * wave1
        try: # if subwave 3 is completed
            return self.iii.end + fib_ratio * self.i.size
        except TypeError:
            try: # predict p3 first
                return self.predict_wave3()+ fib_ratio * self.i.size
            except TypeError:
                return 0
    def predict_wave5from4(self,fib_ratio=1.0):               # wave5 = 1.0 * wave1
        try: # if subwave 4 is completed
            return self.iv.end + fib_ratio * self.i.size
        except TypeError:
            return 0
    def predict_wave5from4s(self,fib_ratio=0.618):               # wave5 = 1.0 * wave1
        try: # if subwave 4 is completed
            return self.iv.end + fib_ratio * self.iii.size
        except TypeError:
            return 0


class Diagonal(Motive):
    pass
class ZigZag(Corrective): # 5-3-5
    pass
class Flat(Corrective): # 3-3-5
    pass
class Double_ZigZag(Corrective): # 3-3-3
    pass
class Triangle(Corrective): # 3-3-3-3-3
    pass
class UFW(Wave):  # UnidentiFied Wave 
    pass


if __name__ == '__main__':
    # set super wave [V]
    superV     = Impulse(start=6450,end=None,level=+1,No=5)
    primary1   = Impulse(start=6450,end=12391,level=0,No=1)
    primary2  = ZigZag(start=12391,end=10404,level=0,No=2)
    primary3 = Impulse(start=10404,end=18351,level=0,No=3)
    primary4  = Flat(start=18351,end=15450,level=0,No=4)
    primary5   = Impulse(start=15450,end=None,level=0,No=5)
    superV.set_subwaves(primary1,primary2,primary3,primary4,primary5)
    # set primary waves I,II,III,IV,V
    superV.i.create_subwaves(6450,8877,8077,11258,9614,12391,Impulse,ZigZag,Impulse,Flat,Impulse)
    superV.ii.create_subwaves(12351,11556,12876,10404,ZigZag,ZigZag,Impulse)
    superV.iii.create_subwaves(10404,13300,12035,16588,15355,18351,Impulse,Flat,Impulse,Flat,Impulse)
    superV.iv.create_subwaves(18351,15370,17987,15450,Impulse,ZigZag,Impulse)
    superV.v.create_subwaves(15450,18167,17140,21170,None,None,Impulse,ZigZag,Impulse,Flat,Impulse)
    #superV.v.set_subwaves(15450,18167,17140,21170,20375,None,Impulse,ZigZag,Impulse,Flat,Impulse)
    # report
    superV.analyze()

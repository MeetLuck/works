# Super waves          [I],[II],[III],...   about decades
# Primary waves        I,II,III,...         about years
# intermediate waves   i,ii,iii,...         about months
# minor waves          <i>,<ii>,<iii>,...   about days

from helper import *

class Wave(object):

    def __new__(cls,*args,**kwargs):
        if cls.__name__ in ('Wave','Motive','Corrective'):
            raise TypeError('cannot instantiate directly')
        return object.__new__(cls,*args,**kwargs)

    def __init__(self,start=None,end=None,level=None,No=None):
        self.start, self.end, self.level, self.No = start,end,level,No
        self.size = None
        self.has_subwaves = False
        self.name = set_name(level,No)
        try:
            self.size = float(end) - float(start)
            self.percent  = 100.0*self.size/self.start
        except: 
            pass
    def __str__(self):
        return '    {name:5} :  {start:8} - {end:<9}\t {size:<7}'\
               .format(name=self.name,start=self.start,end=self.end, size = self.size)

class Motive(Wave):

    def create_subwaves(self,p0,p1,p2,p3,p4,p5,wave1,wave2,wave3,wave4,wave5):
        self.prices = p0,p1,p2,p3,p4,p5
        self.i   = wave1(start=p0,end=p1,level=self.level-1, No=1)
        self.ii  = wave2(start=p1,end=p2,level=self.level-1, No=2)
        self.iii = wave3(start=p2,end=p3,level=self.level-1, No=3)
        self.iv  = wave4(start=p3,end=p4,level=self.level-1, No=4)
        self.v   = wave5(start=p4,end=p5,level=self.level-1, No=5)
        self.subwaves = self.i, self.ii, self.iii, self.iv, self.v
        self.has_subwaves = True

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
        self.set_prices(p0,pa,pb,pc)
        self.set_subwave_types(wave_a,wave_b,wave_c)

    def set_prices(self,p0,pa,pb,pc):
        self.prices = p0,pa,pb,pc

    def set_subwave_types(self,wave_a,wave_b,wave_c):
        try: 
            p0,pa,pb,pc = self.prices
        except AttributeError as error:
            print '%s -> call self.set_prices(...) first' %error
        self.a = wave_a(start=p0,end=pa,level=self.level-1, No=6)
        self.b = wave_b(start=pa,end=pb,level=self.level-1, No=7)
        self.c = wave_c(start=pb,end=pc,level=self.level-1, No=8)
        self.subwaves = self.a, self.b, self.c
        self.has_subwaves = True

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
    #w1 = Wave(start=6450,end=None,level=+1,No=5)
    w2 = Motive(start=6450,end=None,level=+1,No=5)
    #w3 = Corrective(start=6450,end=None,level=+1,No=5)
    superV = Impulse(start=6450,end=None,level=+1,No=5)
    superV.create_subwaves(6450,12391,10404,18351,15450,None,Impulse,ZigZag,Impulse,Flat,Impulse)
    # set primary waves I,II,III,IV,V
    superV.i.create_subwaves(6450,8877,8077,11258,9614,12391,Impulse,ZigZag,Impulse,Flat,Impulse)
    superV.ii.create_subwaves(12351,11556,12876,10404,ZigZag,ZigZag,Impulse)
    superV.iii.create_subwaves(10404,13300,12035,16588,15355,18351,Impulse,Flat,Impulse,Flat,Impulse)
    superV.iv.create_subwaves(18351,15370,17987,15450,Impulse,ZigZag,Impulse)
    superV.v.create_subwaves(15450,18167,17140,21170,None,None,Impulse,ZigZag,Impulse,Flat,Impulse)
    #superV.v.set_subwaves(15450,18167,17140,21170,20375,None,Impulse,ZigZag,Impulse,Flat,Impulse)
    # report
    print_title(fg.RED,'super-wave {name}'.format(name=superV.name))
    overview(superV)
    print_fibs(superV)
    print_fibs_interwaves(superV)
    print_predictions(superV)
    for sub in superV.subwaves:
        print_title(fg.BLUE,'primary-wave {name}'.format(name=sub.name))
        overview(sub)
        if sub.No in [2,4]: continue
        print_fibs(sub)
        print_predictions(sub)

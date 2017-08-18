from helper import *

class Wave:
    def __init__(self,start=None,end=None,level=None,No=None):
        self.start, self.end, self.level, self.no = start,end,level,No
        self.size = None
        self.name = set_name(level,No)
    def __str__(self):
        return '    {name:5} :  {start:8} - {end:<9}\t {size:<7}'.format(name=self.name,start=self.start,end=self.end, size = self.size)

class Motive(Wave):
    def set_prices(self,p0,p1,p2,p3,p4,p5):
        self.prices = p0,p1,p2,p3,p4,p5
    def set_subwaves(self,*wavetypes):
        wave1,wave2,wave3,wave4,wave5 = wavetypes
        try: 
            p0,p1,p2,p3,p4,p5 = self.prices
        except AttributeError as error:
            print '%s -> call self.set_prices(...) first' %error
        self.i   = wave1(start=p0,end=p1,level=self.level-1, No=1)
        self.ii  = wave2(start=p1,end=p2,level=self.level-1, No=2)
        self.iii = wave3(start=p2,end=p3,level=self.level-1, No=3)
        self.iv  = wave4(start=p3,end=p4,level=self.level-1, No=4)
        self.v   = wave5(start=p4,end=p5,level=self.level-1, No=5)
        self.subwaves = self.i,self.ii, self.iii,self.iv,self.v
        self.has_subwaves = True

class Corrective(Wave): # ZigZag, Flat, Double ZigZag
    def set_subwaves(self,wavetypes):
        waveA,waveB,waveC= wavetypes
        p0,pa,pb,pc= self.prices.values()
        self.a = waveA(p0,pa)
        self.b = waveB(pa,pb)
        self.c = waveC(pb,pc)

class Impulse(Motive):
    def report(self):
        print str(self)
        print fg.WHITE + '-'*70
        if self.has_subwaves:
            for subwave in self.subwaves: print subwave
    pass

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


if __name__ == '__main__':
    superV = Impulse(start=6450,end=None,level=+1,No=5)
    superV.set_prices(6450,12391,10404,18351,15450,None)
#   superV.set_prices(p0=6450,p1=12391,p2=10404,p3=18351,p4=15450,p5=None)
    superV.set_subwaves(Impulse,ZigZag,Impulse,Flat,Impulse)
    superV.report()

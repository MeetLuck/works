# Elliot Wave 
import colorama
from colorama import Fore as fg, Back as bg, Style as stl
colorama.init(autoreset=True)

def set_name(level,no): # <i> -> i -> I -> [I]
    assert isinstance(no,int),'no must be 1,2,3,...8'
    literals = 'unused','I','II','III','IV','V','A','B','C'
    if   level == +1: name = '[' + literals[no]+ ']'
    elif level == 0:  name = literals[no] 
    elif level == -1: name = literals[no].lower() 
    elif level == -2: name = '<'+literals[no].lower()+'>'
    else:             name = 'Undefined'
    return name

def print_data(title, data,fg = fg.WHITE,bg=bg.BLACK):
    print fg + bg + '    {title} : {data:5.2f}   '.format(title=title,data=data)
def print_title(color,title):
    print color + '\n{:^60}\n'.format(title)
def print_subtitle(color,title,name):
    print color + '\n{title} {name}'.format(title=title,name=name)

class Wave(object):
    def __init__(self,start,end=None,level=None,no=None):
        '''
        INTERMEDIATE (i,ii,...,v) -> PRIMARY (I,II,..,V) -> SUPER [I],[II],[III],[IV],[V]
        level -1 for intermediate, level 0 for primary, level 1 for super wave  
        no 1,2,3,4,5 for motive, no 6,7,8 for corrective wave
        '''
        self.start, self.end, self.level, self.no =  start, end, level, no 
        self.name = set_name(level,no)
        self.subwaves     = None
        self.size         = None
        self.has_subwaves = False
        self.complete     = False
        if self.start: self.start = float(start)
        if self.end:   self.end   = float(end)
        if self.start and self.end:
            self.complete = True
            self.size     = self.end - self.start
            self.percent  = 100.0*self.size/self.start
    def __str__(self):
        return '    {name:5} :  {start:8} - {end:<9}\t {size:<7}'.format(name=self.name,start=self.start,end=self.end, size = self.size)

class Motive(Wave): # wave I, III, V, A,C

    def set_subwaves(self,start,p1=None,p2=None,p3=None,p4=None,p5=None):
        self.i   = Motive(start=start, end=p1, level=self.level-1, no=1)
        self.ii  = Corrective(start=p1, end=p2, level=self.level-1, no=2)
        self.iii = Motive(start=p2,    end=p3, level=self.level-1, no=3)
        self.iv  = Corrective(start=p3, end=p4, level=self.level-1, no=4)
        self.v   = Motive(start=p4,    end=p5, level=self.level-1, no=5)
        self.subwaves = self.i, self.ii, self.iii, self.iv, self.v
        self.has_subwaves = True

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

    def fibs_interwaves(self,sub_y,yNo,sub_x,xNo): # subwave_y[wave No]/subwave_x[wave No]
        subwave_y, subwave_x = self.subwaves[sub_y-1], self.subwaves[sub_x-1]
        return subwave_y.subwaves[yNo-1].size/subwave_x.subwaves[xNo-1].size

    def fib_wave35from12(self):
        return (self.v.end - self.iii.end)/(self.ii.end - self.i.start)

    def predict_wave3(self,fib_ratio=2.0):                    # wave3 = 2.0 * wave1
        #if not self.i.complete: return None
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

    def print_fibs(self):
        fib20 = fib21 = fib31 = fib43 = fib51 = fib238 = 0
        if self.ii.complete:  fib21 = self.fib(2,1)
        if self.iii.complete: fib31 = self.fib(3,1); fib20 = self.fib20()
        if self.iv.complete:  fib43 = self.fib(4,3)
        if self.v.complete:   fib51 = self.fib(5,1); fib238 = self.fib238()
        print_subtitle(fg.GREEN,'Fibonacci rato for wave',self.name)
        print '    II/I : {fib21:<9.2f} III/I : {fib31:<8.2f} IV/III : {fib43:<8.2f} V/I : {fib51:<8.2f}'\
              .format(fib31=fib31,fib21=fib21,fib43=fib43,fib51=fib51)
        print '    fib2.0 :{fib20:5.2f}    fib2.38 :{fib238:5.2f}'.format(fib20=fib20,fib238=fib238)

    def print_fibs_interwaves(self):
        print_subtitle(fg.GREEN,'Fibonacci ratio between inter-waves for', 'e.g. III.i/I.i') 
        sub_31to11 = self.fibs_interwaves(3,1,1,1)
        sub_31to13 = self.fibs_interwaves(3,1,1,3)
        sub_51to11 = self.fibs_interwaves(5,1,1,1)
        sub_33to13 = self.fibs_interwaves(3,3,1,3)
        sub_53to13 = self.fibs_interwaves(5,3,1,3)
        print_data('III(1)/I(3)', sub_31to13)    
        print_data('III(1)/I(1)', sub_31to11)    
        print_data('V(1)/I(1)  ', sub_51to11)    
        print_data('III(3)/I(3)', sub_33to13)    
        print_data('V(3)/I(3)  ', sub_53to13)    

    def predict_waves(self):
        # predict wave 5
        print_subtitle(fg.YELLOW,'predict p3 and p5 for wave',self.name)
        predict_p3from_p1 = predict_p5from_p1 = predict_p5from_p2 = predict_p5from_p3 =predict_p5from_p4 = 0

        if self.i.complete:   p3from_p1  = self.predict_wave3(fib_ratio=2.0)
        if self.i.complete:   p5from_p1  = self.predict_wave5from1(fib_ratio=2.382)
        if self.ii.complete:  p5from_p2  = self.predict_wave5from2()
        if self.iii.complete: p5from_p3  = self.predict_wave5from3(fib_ratio=0.382)
        if self.iv.complete:  p5from_p4  = self.predict_wave5from4(fib_ratio=1.0)
        print_data('p3 -> 2.0*i         ', p3from_p1)
        print_data('p5 -> 2.382*i       ', p5from_p1)
        print_data('p5 = p3 + (p2-start)', p5from_p2, fg = fg.CYAN)
        print_data('p5 = p3 + 0.382*i   ', p5from_p3)
        print_data('p5 = p4 + 1.0*i     ', p5from_p4)


class Diagonal(Wave): # wave I, III, V, A,C
    pass
class ZigZag(Wave): # wave II,IV,A,B,C
    def set_subwaves(self, start = None, pa=None, pb=None,pc=None):
        self.a = Impulse(start=start,end=pa,level=self.level-1, no = 6)
        self.b = ZigZag( start=pa,   end=pb,level=self.level-1, no = 7)
        self.c = Impulse(start=pb,   end=pc,level=self.level-1, no = 8)
class Flat(Wave):  # wave II, IV, A,B,C
    def set_subwaves(self, start = None, pa=None, pb=None,pc=None):
        self.a = ZigZag( start=start,end=pa,level=self.level-1, no = 6)
        self.b = ZigZag( start=pa,   end=pb,level=self.level-1, no = 7)
        self.c = Impulse(start=pb,   end=pc,level=self.level-1, no = 8)
class Triangle(Wave): # wave II, IV, B
    pass

class Corrective(ZigZag,Flat): # zigzag(5-3-5), flat(3-3-5), double-zigzag(3-3-3), triangle(3-3-3-3-3)
    def set_subwaves(self, start = None, pa=None, pb=None,pc=None, kind=0):
        if   kind == 0:
            ZigZag.set_subwaves(self,start,pa,pb,pc)
        elif kind == 1:
            Flat.set_subwaves(self,start,pa,pb,pc)
        self.has_subwaves = True
        self.subwaves = self.a, self.b, self.c

class Corrective(Wave):
    def set_subwaves(self, start, pa, pb,pc):
        if zigzag: # 5-3-5
            self.a = Motive(start,pa)
            self.b = Corrective(pa,pb)
            self.c = Motive(pb,pc)
        elif flat: # 3-3-5
            self.a = Corrective(start,pa)
            self.b = Corrective(pa,pb)
            self.c = Motive(pb,pc)
        elif double_zigzag: # 3-3-3
            self.a = Corrective(start,pa)
            self.b = Corrective(pa,pb)
            self.c = Corrective(pb,pc)

        self.has_subwaves = True
        self.subwaves = self.a, self.b, self.c


# Elliot Wave Analysis [V] #
#   start       wave I         wave II         wave III        wave IV         wave V
# 6450(0) -> 12391(+5951) -> 10404(-1987) -> 18351(+7906) -> 15450(-2906) -> 20401?(+5941?)

# super waves(level +1)         :  [I]  [II]  [III]  [IV]  [V]   ...  [A] [B] [C] (about decade(10 years) )
# primary waves(level 0)        :   I    II    III    IV    V    ...  A B C for [II], [IV](about serveral years)
# intermediate waves(level -1)  :   i    ii    iii    iv    v    ...  a b c for II, IV (about serveral months)
import sys
sys.path.append('../elliot')

from elliot40 import *

class superV(Motive):
    def __init__(self):
        Motive.__init__(self,start=6450,end=None,level=+1,no=5)
        self.set_motives(start=6450,p1=12391,p2=10404,p3=18351,p4=15450,p5=None)
        self.set_primaries()

    def set_primaries(self):
        '''
        wave I   : 6450  - 8877(p1)  - 8077(p2)  - 11258(p3) - 9614(p4) - 12391(p5)
        wave II  : 12391 - 11556(a)  - 12876(b)  - 10404(c)
        wave III : 10404 - 13662(p1) - 12471(p2) - 17279(p3) - 15885(p4) - 18351(p5)
                   10404 - 13300(p1) - 12035(p2) - 16588(p3) - 15355(p4) - 18351(p5)
        wave IV  : 18351 - 15370(a)  - 17987(b)  - 15450(c)
        wave V   : 15450 - 18167(p1) - 17140(p2) - 21170(p3) - 20375(p4) - ?(p5)
        '''
        #self.i.set_motives(start=6450,p1=8877,p2=8077,p3=11258,p4=9614,p5=12391)
        self.i.set_motives(start=6450,p1=8877,p2=8077,p3=10729,p4=9614,p5=12391)
        self.ii.set_correctives(start=12351,pa=11556,pb=12876,pc=10404)
        #self.iii.set_motives(start=10404,p1=13662,p2=12471,p3=17279,p4=15885,p5=18351)
        self.iii.set_motives(start=10404,p1=13300,p2=12035,p3=16588,p4=15355,p5=18351)
        self.iv.set_correctives(start=18351,pa=15370,pb=17987,pc=15450)
        self.v.set_motives(start=15450,p1=18167,p2=17140,p3=21170,p4=20375,p5=None)

    def get_fibs_for_primary(self,wave_no):
        assert wave_no in [1,3,5],'impulse wave need'
        fib21 = fib31 = fib43 = fib51 = fib20 = fib238 = fib3512 = 0
        if self.subwaves[wave_no-1].i.complete:   fib20 = self.subwaves[wave_no-1].fib20()
        if self.subwaves[wave_no-1].ii.complete:  fib21 = self.subwaves[wave_no-1].fib(2,1)
        if self.subwaves[wave_no-1].iii.complete: fib31 = self.subwaves[wave_no-1].fib(3,1)
        if self.subwaves[wave_no-1].iv.complete:  fib43 = self.subwaves[wave_no-1].fib(4,3)
        if self.subwaves[wave_no-1].v.complete:
            fib51 = self.subwaves[wave_no-1].fib(5,1)
            fib238 = self.subwaves[wave_no-1].fib238()
            fib3512 = self.subwaves[wave_no-1].fib_wave35from12()
        wave_name = self.subwaves[wave_no-1].name
        print fg.GREEN + '\nFibonacci ratio for wave {wave_name}'.format(wave_name=wave_name)
        print '    II/I : {fib21:<9.2f} III/I : {fib31:<8.2f} IV/III : {fib43:<8.2f} V/I : {fib51:<8.2f}'\
              .format(fib31=fib31,fib21=fib21,fib43=fib43,fib51=fib51)
        print '    fib2.0 :{fib20:5.2f}    fib2.38 :{fib238:5.2f}   fib3512 :{fib3512:5.2f}'.format(fib20=fib20,fib238=fib238,fib3512=fib3512)

    def get_fibs_at_interlevel(self):
        print fg.GREEN + '\nFibonacci ratio at inter-level for e.g.  III.i/I.i'
        sub_31to11 = self.fib_interwaves(3,1,1)
        print '    III.i/I.i :{sub_31to11:6.2f}'.format(sub_31to11=sub_31to11)
        sub_51to11 = self.fib_interwaves(5,1,1)
        print '    V.i/I.i   :{sub_51to11:6.2f}'.format(sub_51to11=sub_51to11)

    def predict_wave(self):
        # predict wave 5
        print fg.YELLOW + '\npredict wave for e.g wave5(p5)'
        predict_p5from_p1  = self.predict_wave5from1(fib_ratio=2.382)
        print '    p5 = 2.382p1      : {predict_p5from_p1:5.2f}'.format(predict_p5from_p1 = predict_p5from_p1)
        predict_p5from_p2  = self.predict_wave5from2()
        print '    p5 = p3 + (p2-start) : {predict_p5from_p2:5.2f}'.format(predict_p5from_p2 = predict_p5from_p2)
        predict_p5from_p3  = self.predict_wave5from3(fib_ratio=0.382)
        print '    p5 = p3 + 0.382p1 : {predict_p5from_p3:5.2f}'.format(predict_p5from_p3 = predict_p5from_p3)
        predict_p5from_p4  = self.predict_wave5from4(fib_ratio=1.12)
        print '    p5 = p4 + 1.0p1   : {predict_p5from_p4:5.2f}'.format(predict_p5from_p4 = predict_p5from_p4)

print fg.RED +'superwave [V] Analysis : I,II,III,IV,V\n'
superwaveV = superV()
superwaveV.report()
superwaveV.print_fibs()
superwaveV.get_fibs_at_interlevel()
superwaveV.predict_wave()
#print fg.RED +'\n\nprimary I Analysis\n'
print_title(fg.RED,'primary I Analysis')
superwaveV.i.report()
superwaveV.i.print_fibs()
print_title(fg.RED,'primary III Analysis')
superwaveV.iii.report()
superwaveV.print_fibs()
print_title(fg.RED,'primary V Analysis')
superwaveV.v.report()
superwaveV.get_fibs_for_primary(5)


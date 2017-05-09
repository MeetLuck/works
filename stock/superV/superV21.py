# Elliot Wave Analysis [V] #
#   start       wave I         wave II         wave III        wave IV         wave V
# 6450(0) -> 12391(+5951) -> 10404(-1987) -> 18351(+7906) -> 15450(-2906) -> 20401?(+5941?)

# super waves(level +1)         :  [I]  [II]  [III]  [IV]  [V]   ...  [A] [B] [C] (about decade(10 years) )
# primary waves(level 0)        :   I    II    III    IV    V    ...  A B C for [II], [IV](about serveral years)
# intermediate waves(level -1)  :   i    ii    iii    iv    v    ...  a b c for II, IV (about serveral months)
import sys
sys.path.append('../elliot')

from elliot22 import *

class superV:
    def __init__(self):
        self.wave = Motive(start=6450,end=None,level=+1,no=5)
        self.wave.set_motives(start=6450,p1=12391,p2=10404,p3=18351,p4=15450,p5=None)
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
        self.wave.i.set_motives(start=6450,p1=8877,p2=8077,p3=11258,p4=9614,p5=12391)
        self.wave.ii.set_correctives(start=12351,pa=11556,pb=12876,pc=10404)
        self.wave.iii.set_motives(start=10404,p1=13662,p2=12471,p3=17279,p4=15885,p5=18351)
        #self.wave.iii.set_motives(start=10404,p1=13300,p2=12035,p3=16588,p4=15355,p5=18351)
        self.wave.iv.set_correctives(start=18351,pa=15370,pb=17987,pc=15450)
        self.wave.v.set_motives(start=15450,p1=18167,p2=17140,p3=21170,p4=20375,p5=None)
    def get_fibs(self):
        fib21 = self.wave.fib(2,1)
        fib31 = self.wave.fib(3,1)
        fib43 = self.wave.fib(4,3)
        fib51 = self.wave.fib(5,1)
        fib20 = self.wave.fib20()
        if self.wave.complete: fib238 = self.wave.fib238()
        else: fib238 = 0
        print
        print 'Fibonacci ratio for wave {wave_name}'.format(wave_name=self.wave.name)
        print '    wave II/I : {fib21:<9.2f} wave III/I : {fib31:<8.2f} wave IV/III : {fib43:<8.2f} wave V/I : {fib51:<8.2f}'\
              .format(fib31=fib31,fib21=fib21,fib43=fib43,fib51=fib51)
        print '    fib2.0  :{fib20:5.2f}'.format(fib20=fib20)
        print '    fib2.38 :{fib238:5.2f}'.format(fib238=fib238)
    def get_fibs_for_primary(self,wave_no):
        if wave_no in [1,3,5]:
            fib21 = self.wave.subwaves[wave_no-1].fib(2,1)
            fib31 = self.wave.subwaves[wave_no-1].fib(3,1)
            fib43 = self.wave.subwaves[wave_no-1].fib(4,3)
            fib51 = self.wave.subwaves[wave_no-1].fib(5,1)
            fib20 = self.wave.subwaves[wave_no-1].fib20()
            if self.wave.subwaves[wave_no-1].complete:
                fib238 = self.wave.subwaves[wave_no-1].fib238()
            else:
                fib238 = 0
            wave_name = self.wave.subwaves[wave_no-1].name
            print
            print 'Fibonacci ratio for wave {wave_name}'.format(wave_name=wave_name)
            print '    wave II/I : {fib21:<9.2f} wave III/I : {fib31:<8.2f} wave IV/III : {fib43:<8.2f} wave V/I : {fib51:<8.2f}'\
                  .format(fib31=fib31,fib21=fib21,fib43=fib43,fib51=fib51)
            print '    fib2.0  :{fib20:5.2f}'.format(fib20=fib20)
            print '    fib2.38 :{fib238:5.2f}'.format(fib238=fib238)
        elif wave_no in [2,4]:
            print 'not implemented'

    def get_fibs_at_interlevel(self):
        print
        print 'Fibonacci ratio at inter-level for e.g.  III.i/I.i'
        sub_31to11 = self.wave.fib_subwaves(3,1,1)
        print '    wave III.i/I.i :{sub_31to11:6.2f}'.format(sub_31to11=sub_31to11)
        sub_51to11 = self.wave.fib_subwaves(5,1,1)
        print '    wave V.i/I.i   :{sub_51to11:6.2f}'.format(sub_51to11=sub_51to11)
    def predict_wave(self):
        # predict wave 5
        print
        print 'predict wave for e.g wave5(p5)'
        predict_p5from_p1  = self.wave.predict_wave5from1(fib_ratio=2.382)
        print '    predict p5 from p1 : {predict_p5from_p1:5.2f}'.format(predict_p5from_p1 = predict_p5from_p1)
        predict_p5from_p2  = self.wave.predict_wave5from2()
        print '    predict p5 from p2 : {predict_p5from_p2:5.2f}'.format(predict_p5from_p2 = predict_p5from_p2)
        predict_p5from_p3  = self.wave.predict_wave5from3(fib_ratio=0.382)
        print '    predict p5 from p3 : {predict_p5from_p3:5.2f}'.format(predict_p5from_p3 = predict_p5from_p3)
        predict_p5from_p4  = self.wave.predict_wave5from4(fib_ratio=1.12)
        print '    predict p5 from p4 : {predict_p5from_p4:5.2f}'.format(predict_p5from_p4 = predict_p5from_p4)


print fg.RED +'superwave [V] Analysis : I,II,III,IV,V'
superwaveV = superV()
superwaveV.wave.report()
superwaveV.get_fibs()
superwaveV.get_fibs_at_interlevel()
superwaveV.get_fibs_for_primary(1)
superwaveV.get_fibs_for_primary(3)
superwaveV.get_fibs_for_primary(5)
superwaveV.predict_wave()


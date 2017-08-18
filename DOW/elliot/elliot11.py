# Elliot Wave Analysis [V] #
#   start       wave I         wave II         wave III        wave IV         wave V
# 6450(0) -> 12391(+5951) -> 10404(-1987) -> 18351(+7906) -> 15450(-2906) -> 20401?(+5941?)

import colorama
from string import Template
from colorama import Fore as fg, Back as bg, Style as stl
colorama.init(autoreset=True)


class Wave:
    def __init__(self,start,end):
        self.start,self.end = float(start), float(end)
        self.compute_wave()
    def compute_wave(self):
        self.size = self.end - self.start
        self.percent = 100.0*self.size/self.start

class EWaves:
    def __init__(self, *waves):
        if 1 <= len(waves) <= 4:
            self.predict(waves)
        elif len(waves) == 5:
            self.analyze(waves)
            self.predict( waves[0:3] ) # wave1,wave2,wave3,wave4 = waves[0:3]
        else:
            raise Exception('waves not avaiable')
    def predict(self,waves):
        # get wave1,wave2,..., a,b,c,...
        if len(waves) >= 1:
            wave1 = waves[0]; a = wave1.size
        if len(waves) >= 2:
            wave2 = waves[1]; b = wave2.size
        if len(waves) >= 3:
            wave3 = waves[2]; c = wave3.size
        if len(waves) >= 4:
            wave4 = waves[3]; d = wave4.size
        # compute wave
        if len(waves) >= 1: # wave1,...
            self.predict_wave3(wave1,a)
        if len(waves) >= 3: # wave3,...
            self.predict_wave4(wave1,wave2,wave3,a,b,c)
        if len(waves) >= 4: # wave4,...
            self.predict_wave5(wave1,wave2,wave3,wave4,a,b,c,d)
    def predict_wave3(self,wave1,a):
        ''' predict wave 3 and wave 5 based on Fibnacci ratio such as 2.0a,2.38a '''
        p0,p1 = wave1.start, wave1.end
        p3,p5 = p1 + 1.0*a, p1 + 1.382*a
        print 
        print fg.CYAN + bg.WHITE + '\t{:70}'.format('predict Wave III = 2.0*I and Wave V = 2.38*I')
        print fg.CYAN + '< Wave I : %d - %d >' %(p0,p1)
        print 'p1 : %d\t' %p1,fg.YELLOW+'p3 : %d\tp5 : %d' %(p3,p5)
#       print 'p1 : %d\tp3 : %d\t p5 : %d' %(p1,p3,p5)
    def predict_wave4(self,wave1,wave2,wave3,a,b,c):
        ''' predict wave IV = waveIII - 0.618a '''
        p0,p1,p2,p3 = wave1.start, wave1.end, wave2.end, wave3.end
        p4 = p3 - c/2.382
        p5 = p4 + a
        print fg.CYAN + bg.WHITE + '\t{:70}'.format('predict wave IV = III - III/2.382')
        print fg.CYAN + '< Wave I-III: %d - %d >' %(p0,p3)
        print 'p1 : %d\tp2 : %d\tp3 : %d\t' %(p1,p2,p3),fg.YELLOW + 'p4 : %d\tp5 : %d' %(p4,p5)
        wave4 = Wave(p3,p4)
        wave5 = Wave(p4,p5)
        waves = wave1,wave2,wave3,wave4,wave5
        self.analyze(waves)

    def predict_wave5(self,wave1,wave2,wave3,wave4,a,b,c,d):
        ''' predict wave V = IV + 1.0*I '''
        p0,p1,p2,p3,p4 = wave1.start, wave1.end, wave2.end,wave3.end, wave4.end
        p5 = p4 + 1.0*a
        # predict wave III based on wave I
        print fg.CYAN + bg.WHITE + '\t{:70}'.format('predict wave V = IV + 1.0*I')
        print fg.CYAN + '< Wave I-IV: %d - %d >' %(p0,p4)
        print 'p1 : %d\tp2 : %d\tp3 : %d\tp4 : %d\t' %(p1,p2,p3,p4),fg.YELLOW + 'p5 : %d' %p5

    def analyze(self,waves):
        wave1,wave2,wave3,wave4,wave5 = waves
        p0,p1,p2,p3,p4,p5 = wave1.start,wave1.end,wave2.end,wave3.end,wave4.end,wave5.end
        a = wave1.size; b = wave2.size; c = wave3.size; d = wave4.size; e = wave5.size
        self.Fib_2 = b/a
        self.Fib_3 = c/a
        self.Fib_4 = d/c
        self.Fib_5 = e/a
        print
        print fg.GREEN + bg.WHITE +'\t{:70}'.format('analyze Elliot Wave')
        print fg.GREEN +'< Wave started at {p0}>'.format(p0 = p0)
        prices = 'p1 : {p1:<9} p2 : {p2:<9} p3 : {p3:<9} p4 : {p4:<9} p5 : {p5:<9}'\
                .format( p1=int(p1),p2=int(p2),p3=int(p3),p4=int(p4),p5=int(p5) )
        print prices
        print fg.GREEN +'< Sizes >'
        print 'a : {a:<10} b : {b:<10} c : {c:<10} d : {d:<10} e : {e:<10}'.format(a=int(a), b=int(b), c=int(c),d=int(d),e=int(e))
        print fg.GREEN +'<Fib ratio Analysis I for 1.618, 0.618, 0.382, 1.0 or 0.618>'
        print 'b/a : %.2f\tc/a : %.2f\td/c: %.2f\te/a : %.2f' %(self.Fib_2, self.Fib_3, self.Fib_4, self.Fib_5)
        print fg.GREEN +'<Fib ratio Analysis II for 2.0(wave3), 2.38(wave5)>'
        print '2.0 : %.2f\t2.38 : %.2f' %( (a+b+c)/a, (a+b+c+d+e)/a )

if __name__ == '__main__':
    def analyze_waveV3():
        '''  wave V.3 analysis '''
        wave1 = Wave(17063,18622)
        wave2 = Wave(18622,17884)
        wave3 = Wave(17884,19909)
        wave4 = Wave(19909,19668)
        wave5 = Wave(19668,21169)
        ew = EWaves(wave1,wave2,wave3,wave4,wave5)
    def predict_waveV():
        ''' predict wave 3 of wave V '''
        wave1 = Wave(15503,18167)
        ew = EWaves(wave1)
#       wave2 = Wave(18167,17063)
    def waveI_II_III_IV_V():
        wave1 = Wave(6450,12391)
        wave2 = Wave(12391,10404)
        wave3 = Wave(10445,18351)
        wave4 = Wave(18351,15450)
        wave5 = Wave(15450,21170)
        ew = EWaves(wave1,wave2,wave3,wave4,wave5)
    # waveI_II_III_IV_V analyze
    waveI_II_III_IV_V()
    # wave V.3 analysis
    analyze_waveV3()
    # wave V predict
    print
    predict_waveV()


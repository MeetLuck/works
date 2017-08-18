# Elliot Wave Analysis [V] #
#   start       wave I         wave II         wave III        wave IV         wave V
# 6450(0) -> 12391(+5951) -> 10404(-1987) -> 18351(+7906) -> 15450(-2906) -> 20401?(+5941?)

# super waves(level +1)         :  [I]  [II]  [III]  [IV]  [V]   ...  [A] [B] [C] (about decade(10 years) )
# primary waves(level 0)        :   I    II    III    IV    V    ...  A B C for [II], [IV](about serveral years)
# intermediate waves(level -1)  :   i    ii    iii    iv    v    ...  a b c for II, IV (about serveral months)
import sys
sys.path.append('../elliot')

from elliot60 import *

def superV():
    def set_primaries():
        # wave I   : 6450  - 8877(p1)  - 8077(p2)  - 11258(p3) - 9614(p4) - 12391(p5)
        # wave II  : 12391 - 11556(a)  - 12876(b)  - 10404(c)
        # wave III : 10404 - 13662(p1) - 12471(p2) - 17279(p3) - 15885(p4) - 18351(p5)
        #          10404 - 13300(p1) - 12035(p2) - 16588(p3) - 15355(p4) - 18351(p5)
        # wave IV  : 18351 - 15370(a)  - 17987(b)  - 15450(c)
        # wave V   : 15450 - 18167(p1) - 17140(p2) - 21170(p3) - 20375(p4) - ?(p5)
        # superwaveV.i.set_motives(start=6450,p1=8877,p2=8077,p3=11258,p4=9614,p5=12391)
        superwaveV.i.set_subwaves(start=6450,p1=8877,p2=8077,p3=10729,p4=9614,p5=12391)
        superwaveV.ii.set_subwaves(start=12351,pa=11556,pb=12876,pc=10404,kind=1)
        superwaveV.iii.set_subwaves(start=10404,p1=13300,p2=12035,p3=16588,p4=15355,p5=18351)
        #superwaveV.iii.set_motives(start=10404,p1=13662,p2=12471,p3=17279,p4=15885,p5=18351)
        superwaveV.iv.set_subwaves(start=18351,pa=15370,pb=17987,pc=15450,kind=0)
        superwaveV.v.set_subwaves(start=15450,p1=18167,p2=17140,p3=21170,p4=20375,p5=None)

#   print fg.RED +'superwave [V] Analysis : I,II,III,IV,V\n'
    print_title(fg.RED,'superwave [V] Analysis')
    superwaveV = Impulse(start=6450, end=None, level=+1, No=5) 
    superwaveV.create_subwaves(p0=6450,p1=12391,p2=10404,p3=18351,p4=15450,p5=None)
    set_primaries()
    superwaveV.report()
    superwaveV.print_fibs()
    superwaveV.print_fibs_interwaves()
    superwaveV.predict_waves()
    #print fg.RED +'\n\nprimary I Analysis\n'
    for subwave in superwaveV.subwaves:
        if subwave.no in [2,4]: continue
        print_title(fg.RED,'primary {name} Analysis'.format(name=subwave.name))
        subwave.report()
        subwave.print_fibs()
        subwave.predict_waves()

if __name__ == '__main__':
    superV()

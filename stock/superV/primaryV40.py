import os,sys
#os.chdir( os.path.abspath(os.path.dirname(__file__)) )
sys.path.append('../elliot')

from elliot40 import *

def primaryV():
    # 15450 - 18167(p1) - 17063(p2) - 21170(p3) - 20375?(p4) - ?(p5)
    # 15450 - 18662(p1) - 17883(p2) - 21170(p3) - 20375?(p4) - ?(p5)
    #  wave iii analysis 
    # 17063 - 18668(p1) - 17884(p2) - 19909(p3) - 19668(p4) - 21170(p5)
    # a = 1605, b = -784, c = 2025, d = -241, e = 1502
    def set_intermediates():
        # wave i   : Unidentified
        # wave ii  : Unidentified
        # wave iii : 17063 - 18668(p1) - 17884(p2) - 19909(p3) - 19668(p4) - 21170(p5)
        # wave iv  : Unidentified
        # wave v   : 20375 - 21075(p1) - 20850(p2) - ?(p3) - ?(p4) - ?(p5)
        primaryV.i.set_motives(start=15450,p1=None,p2=None,p3=None,p4=None,p5=18668)
        primaryV.ii.set_correctives(start=18668,pa=17331,pb=18011,pc=17063)
        primaryV.iii.set_motives(start=17063,p1=18668,p2=17884,p3=19909,p4=19668,p5=21170)
        primaryV.iv.set_correctives(start=21170,pa=20413,pb=20887,pc=20375)
        primaryV.v.set_motives(start=20375,p1=21075,p2=20850,p3=None,p4=None,p5=None)

    print_title(fg.RED,'Primary wave V of [V] Analysis')
    primaryV = Motive(start=15450, end=None, level=0, no=5) 
    primaryV.set_motives(start=15450,p1=18167,p2=17140,p3=21170,p4=20375,p5=None)
    set_intermediates()
    primaryV.report()
    primaryV.print_fibs()
#   primaryV.print_fibs_interwaves()
    primaryV.predict_waves()
    for subwave in primaryV.subwaves:
        if subwave.no in [2,4]: continue
        print_title(fg.RED,'intermediate {name} Analysis'.format(name=subwave.name))
        subwave.report()
        subwave.print_fibs()
        subwave.predict_waves()

def alt_primaryV():
    print_title(fg.RED,'alternative Primary wave V of [V] Analysis')
    primaryV = Motive(start=15450, end=None, level=0, no=5) 
    primaryV.set_motives(start=15450,p1=18668,p2=17883,p3=21170,p4=20375,p5=None)
    #set_intermediates()
    primaryV.report()
    primaryV.print_fibs()
    primaryV.predict_waves()

if __name__ == '__main__':
    primaryV()
    print
    alt_primaryV()

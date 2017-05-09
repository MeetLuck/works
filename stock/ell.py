import optparse
from colorama import *
parser = optparse.OptionParser()
parser.add_option('-p','--price',type='float')#,dest='price')
parser.add_option('-e','--estimate',type='float',nargs=2,metavar='<p1> <p2>')#,dest='wave')
parser.add_option('-c','--compute',type='float',nargs=6,metavar='<p1> <p2> <p3> <p4> <p5> <p6>')#,dest='wave')


def print_percent():

    def print_minus():
        print Fore.RED + 'minus percent change'
        for i in range(1,11):
            delta = opts.price*(i * 0.01)
            print Fore.GREEN +'-%d%% : %.1f' %(i, opts.price - delta) 
        print Fore.GREEN +'-38.2%% : %.1f' %( opts.price*(1.0 - 0.382) )
        print Fore.GREEN +'-50.0%% : %.1f' %( opts.price*(1.0 - 0.500) )
        print Fore.GREEN +'-61.8%% : %.1f' %( opts.price*(1.0 - 0.618) )
    print_minus()
    

def estimate_wave():
    p1,p2 = opts.estimate
#    size = abs(p1 - p2)
    a = p2 - p1
    ep3 = p1 + 2*a
    ep5 = p1 + 2.38*a
    print Fore.RED + 'estimate 3rd wave(p3), size(a,c)'
    print Fore.GREEN + 'p1 = %d, p2  = %d\t => %2.1f%%, a = %d' %( p1, p2, 100*a/p1,  a )
    print 'ep3 = %d         \t => %2.1f%%, c = %d' %( ep3, 100*2*a/p1,2*a)
    print 'ep5 = %d         \t => %2.1f%%, e = %d' %( ep5, 100*2.38*a/p1, a)

#   > ell.py -e 21169 20412
#   estimate 3rd wave(p3), size(a,c)
#   p1 = 21169, p2  = 20412  => -3.6%, a = -757
#   ep3 = 19655              => -7.2%, c = -1514

def compute_wave(): 
    p1,p2,p3,p4,p5,p6 = opts.compute
    a = p1 - p2
    b = p2 - p3
    c = p3 - p4
    d = p4 - p5
    e = p5 - p6
    print 'compute wave(1-3-5-7-9), sizes(a,b,c,d,e)'
    print 'p1 = %d, p2  = %d => %2.1f%%, a = %d' %( p1, p2, 100*a/p1,  a )
    print 'p2 = %d, p3  = %d => %2.1f%%, b = %d' %( p2, p3, 100*b/p2,  b )
    print 'p3 = %d, p4  = %d => %2.1f%%, c = %d' %( p3, p4, 100*c/p3,  c )
    print 'p4 = %d, p5  = %d => %2.1f%%, d = %d' %( p4, p5, 100*d/p4,  d )
    print 'p5 = %d, p6  = %d => %2.1f%%, e = %d' %( p5, p6, 100*e/p5,  e )

if __name__ == '__main__':
    opts,args = parser.parse_args()
    if opts.price is None and opts.estimate is None and opts.compute is None:
        parser.print_help()
        exit(-1)
    if opts.price is None and opts.compute is None:
        estimate_wave()
    if opts.estimate is None and opts.compute is None:
        print_percent()
    if opts.price is None and opts.estimate is None:
        compute_wave()
#    argv = '-p 21200'.split()
#    display_percent(argv)

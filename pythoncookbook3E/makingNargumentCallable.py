# 7.8 Making an N-Argument Callable Work as a Callable with Fewer Arguments

from functools import partial
import math

def distance(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return math.hypot(x2-x1,y2-y1)

def distance_test():
    pt = (4,3)
    points = [(1,2),(3,4),(5,6),(7,8)]
    points.sort( key = partial(distance, pt) )
    print points

def output_result(result, log = None):
    try: log.debug('\tGot: %r',result)
    except: pass
def pow(x,y): return x**y

def async_compute():
    import logging
    from multiprocessing import Pool
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('test')
    p = Pool()
    p.apply_async(pow, (3.0,4.0), callback=partial(output_result,log=log) )
    p.close()
    p.join()

if __name__ == '__main__':
#   distance_test()
    async_compute()



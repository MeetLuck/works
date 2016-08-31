def repeatfunc(func, times=None, *args):
   ''' repeat calls to func with specified arguments
       func(*args), func(*args),.....
   '''
   print args
   if times is None: return starmap(func, repeat(args))
   return starmap(func, repeat(args, times) )

if __name__ == '__main__':
    from itertools import *
    args = 10,3
    rf = repeatfunc(pow,3,*args)
    print list(rf)



    

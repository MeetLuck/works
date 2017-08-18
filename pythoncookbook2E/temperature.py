# Converting among Temperature Scales

class Temperature(object):

    coefficients = {'c': (1.0,0.0,-273.15), 'f':(1.8,-273.15,32.0)}

    def __init__(self,**kwargs):
        # default to absolute Kelvin 0, but allow one named argument,
        # with name being k,c,f to use any of the scales
        try:
            name,value = kwargs.popitem()
        except KeyError:
            # no arguments, so default to k=0
            name, value = 'k',0
        # error if there are more arguments, or the arg's name is unknown
        if kwargs or name not in 'kcf':
            kwargs[name] = value # put it back for diagnosis
            raise TypeError,' invalid arguments %r' %kwargs
#       self.__dict__[name] = float(value) 
        setattr(self,name, float(value))

    def __getattr__(self,name):
        # maps getting of c,f to computation from k
        print '__getattr__ %s' %name
        try:
            eq = self.coefficients[name]
        except KeyError:
            # unknown name, give error message
            raise AttributeError, name
        return (self.k + eq[1])* eq[0] + eq[2]
    def __setattr__(self,name,value):
        # maps settings of k,c,f to setting of k; forbids others
        print 'self.%s = %s' %(name,value)
        if name in self.coefficients: # name is c,f -- compute and set k
#           print name
            eq = self.coefficients[name]
            print 'before self.k'
            self.k = (value - eq[2])/eq[0] - eq[1]
            print 'after self.k'
        elif name == 'k': # name is k, just set it
            print 'calling object.__setattr__ %s' %name
#           self.k = value
            object.__setattr__(self,name,value)
        else: # unknown name, give error
            raise AttributeError, name
    def __str__(self): # readable, concise representation as string
        return '%.2f K' %self.k

if __name__ == '__main__':
    t = Temperature(f=70)
#   print t
    t.k
#   print t.c, t.k
#   t.c = 23
#   print t

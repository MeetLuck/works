# Example 5-1 The metaMetaBunch metaclass

import warnings

class MetaBunch(type):

    def __new__(mcl,classname,bases,classdict):

        def __init__(self,**kw):
            for k in self.__dflts__: setattr(self,k,self.__dflts__[k])
            for k in kw: setattr(self,k,kw[k])

        def __repr__(self):
            rep = [ '%s=%r' %(k,getattr(self,k)) for k in self.__dflts__
                    if getattr(self,k)!= self.__dflts__[k] ]
            return '%s(%s)' %(classname,','.join(rep))

        newdict = {'__slot__':list(), '__dflts__':dict(),
                   '__init__':__init__,'__repr__':__repr__,}

        for k in classdict:
            if k.startswith('__') and k.endswith('__'):
                if k in newdict:
                    warnings.warn("Can't set attr %r in bunch-class %r" %(k,classname))
                else:
                    newdict[k] = classdict[k]
            else:
                newdict['__slot__'].append(k)
                newdict['__dflts__'][k] = classdict[k]
        print 'meta class is ',mcl
        print 'class name is ',classname
        print 'bases is ',bases
        print 'class dict is',classdict
        print 'new dict is', newdict
        return super(MetaBunch,mcl).__new__(mcl,classname,bases,newdict)

class Bunch(object):
    __metaclass__ = MetaBunch
    attr = 'bunch attr'
#   def __init__(self,**kw):
#       pass

if __name__ == '__main__':
    print
    print 'Bunch.__dict__:\n',vars(Bunch)
    Bunch.K = '23'
    p1 = Bunch(x=2.3, y= 4.5)
    print
    print 'Bunch.__dict__:\n',vars(Bunch)
    print
    print p1
    print vars(p1)

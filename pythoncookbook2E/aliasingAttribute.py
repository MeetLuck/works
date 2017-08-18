# 20.3 Aliasing Attribute Values
class DefaultAlias(object):
    ''' unless explicitly assigned, this attribute aliases to another '''
    def __init__(self,name):
        self.name = name
    def __get__(self,inst,cls):
        if inst is None: return self
        return getattr(inst,self.name)

class Alias(DefaultAlias):
    def __set__(self,inst,value):
        setattr(inst,self.name,value)
    def __delete__(self,inst):
        delattr(inst,self.name)


class Book(object):

    shortTitle = DefaultAlias('title')

    def __init__(self,title,shortTitle=None):
        self.title = title
        if shortTitle is not None:
            self.shortTitle = shortTitle
    @staticmethod
    def test():
        book = Book('The Life and Opinions of Tristram Shandy')
        print book.shortTitle
        print vars(book)
        book.shortTitle = 'Tristram Shandy'
        print book.shortTitle
        print vars(book)
        del book.shortTitle
        print book.shortTitle
        print vars(book)


import warnings
warnings.simplefilter('default', DeprecationWarning)
#print warnings.filters

class OldAlias(Alias):
    def _warn(self):
#       print 'use %r, not %r' %(self.name, self.oldname)
        warnings.warn('use %r, not %r' %(self.name, self.oldname),DeprecationWarning, stacklevel=2)
    def __init__(self,name,oldname):
        super(OldAlias,self).__init__(name)
        self.oldname = oldname
    def __get__(self,inst,cls):
        self._warn()
        return super(OldAlias,self).__get__(inst,cls)
    def __set__(self,inst,value):
        self._warn()
        return super(OldAlias,self).__set__(inst,value)
    def __delete__(self,inst):
        self._warn()
        return super(OldAlias,self).__delete__(inst)

class NiceClass(object):

    bad_old_name = OldAlias('nice_new_name','bad_old_name')

    def __init__(self,name):
        self.nice_new_name = name

    @staticmethod
    def test():
        x = NiceClass(23)
        for y in range(4):
            print x.bad_old_name
            x.bad_old_name += 100

if __name__ == '__main__':
#   Book.test()
    print
    NiceClass.test()

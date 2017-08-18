# 7.12 Accessing Variables defined Inside a Closure

def function_maker(k=0):
    def func(): 
        print 'n = ',func.n
    def get(): return func.n
    def set(value): func.n = value
    func.n = k
    func.get = get
    func.set = set
    return func

def function_maker_test():
    f = function_maker(k=1)
    f()
    f.set(10)
    f()
    f.get()
    f()

class ClosureInstance(object):
    def __init__(self,locals=None):
        import sys
        if locals is None:
            locals = sys._getframe(1).f_locals
        # update instance dictionary with callables
        print locals.items()
        self.__dict__.update(locals.items())
        #self.__dict__.update( (key,value) for key,value in locals.items() )
    def __len__(self):
        return self.__dict__['__len__']()

def Stack():
    items = []
    def push(item): items.append(item)
    def pop():  return items.pop()
    def __len__(): return len(items)
    return ClosureInstance()

def closure_instance_test():
    s = Stack()
    print repr(s)
    s.push(10); s.push(20); s.push('Hello')
    print len(s)
    print s.pop()
if __name__ == '__main__':
    #function_maker_test()
    closure_instance_test()

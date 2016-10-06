#class A(object):
class A:
    def __init__(self,x):
        self.some_name = x
        print self

    def print_a(self):
        print self.some_name

#class B(object):
class B:
    def __init__(self):
        self.some_name = 'B'
        print self

    def print_b(self):
        print self.some_name

class C(A, B):
    def __init__(self,x):
        print self
        A.__init__(self,x)
        B.__init__(self)

if __name__ == '__main__':
    c = C('www')
    c.print_a()

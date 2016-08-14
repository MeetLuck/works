class A:
    num_of_instance = 0
    def __init__(self):
        self.count()
    @classmethod
    def count(cls):
        cls.num_of_instance += 1
        print '{cls} creates {num} instances'.format(cls=cls,\
                num=cls.num_of_instance)
    @staticmethod
    def print_num_of_instance():
        print A.num_of_instance
class B(A):
    num_of_instance = 0

if __name__ == '__main__':
    a1,a2 = A(), A()
    b1,b2,b3 = B(), B(), B()
    A.print_num_of_instance()
    B.print_num_of_instance()

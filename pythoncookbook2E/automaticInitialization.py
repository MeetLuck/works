# 20.14 Automatic Initialization of Instance Attributes

class Counter(object):
    count = 0
    def increase(self, addend=1):
        print vars(self)
        self.count += addend # instance.count defined here!!!
        print vars(self)

    @staticmethod
    def test():
        print 'ct1: '
        ct1 = Counter()
        ct1.increase(10)
        print 'ct2: '
        ct2 = Counter()
        ct2.increase(3)

if __name__ == '__main__':
    Counter.test()

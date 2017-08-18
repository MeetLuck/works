# 8.16 Defining More than One Constructor in a class

import time
class Date(object):
    # primary constructor
    def __init__(self,year,month,day):
        self.year = year
        self.month = month
        self.day = day
    # ALTERNATE constructor
    @classmethod
    def today(cls):
        t = time.localtime()
        return cls(t.tm_year,t.tm_mon,t.tm_mday)

    def __str__(self):
        return 'Date(%s,%s,%s)' %(self.year,self.month,self.day)

    @staticmethod
    def test():
        a = Date(2017,02,21)
        b = Date.today()
        print a
        print b

if __name__ == '__main__':
    Date.test()

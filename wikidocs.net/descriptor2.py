from __future__ import division
class Temperature(object):
    class Celsius(object):
        def __get__(self,instance,owner):
            return self.celsius
        def __set__(self,instance,C):
            self.celsius = C
    class Fahrenheit(object):
        def __get__(self,instance,owner):
            return instance.celsius * 9/5 + 32
        def __set__(self,instance,F):
            self.fahrenheit = F
            instance.celsius = (self.fahrenheit - 32) * 5/9
    celsius = Celsius()
    fahrenheit = Fahrenheit()

if __name__ == '__main__':
    t = Temperature()
    t.celsius = 10
    print '*'*80
    print t.celsius, t.fahrenheit
    t.fahrenheit = 48 
    print '*'*80
    print t.celsius, t.fahrenheit
         

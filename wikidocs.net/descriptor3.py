from __future__ import division
class Temperature(object):
    def __init__(self, fahrenheit=32):
        self._fahrenheit = fahrenheit
        self._celsius = self.convert_to_celsius(fahrenheit)

    def convert_to_celsius(self, f):
        return (f - 32) * (5 / 9)

    def convert_to_fahrenheit(self, c):
        return (c * (9 / 5)) + 32

    def set_fahrenheit(self, value):
        self._fahrenheit = value
        self._celsius = self.convert_to_celsius(value)

    def set_celsius(self, value):
        self._fahrenheit = self.convert_to_fahrenheit(value)
        self._celsius = value

    def get_fahrenheit(self):
        return int(self._fahrenheit)

    def get_celsius(self):
        return int(self._celsius)

    fahrenheit = property(get_fahrenheit, set_fahrenheit)
    celsius = property(get_celsius, set_celsius)

if __name__ == '__main__':
    t = Temperature()
    t.celsius = 10
    print t.celsius, t.fahrenheit
    t.fahrenheit = 48
    print t.celsius, t.fahrenheit


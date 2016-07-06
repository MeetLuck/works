''' chapter 17: Classes and methods '''
#------------ 17.1 Object-oriented features -------------

#------------ 17.2 Printing objects ---------------------
class Time(object):
    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

    def print_time(time):
        print '%.2d:%.2d:%.2d' %(time.hour, time.minute, time.second)

    def time_to_int(self):
        minutes = self.hour * 60 + self.minute
        seconds = minutes * 60 + self.second
        return seconds
    def increment(self,seconds):
        seconds += seconds
        return int_to_time(seconds)
    #--------- self is more recent than other -----------
    def is_after(self, other):
        return self.time_to_int() > other.time_to_int()
    def __str__(self):
        return '%.2d:%.2d:%.2d' %(self.hour, self.minute,self.second)
    def __add__(self, other):
        if isinstance(other, Time):
            return self.add_time(other)
        else:
            return self.increment(other)
    def add_time(self, other):
        seconds = self.time_to_int() + other.time_to_int()
        return int_to_time(seconds)
    def __radd__(self,other):
        return self.__add__(other)

def int_to_time(seconds):
    minutes,second = divmod(seconds,60)
    hour,minute = divmod(minutes,60)
    return Time(hour, minute, second)


start = Time()
start.hour = 9
start.minute = 45
start.second = 00
Time.print_time(start)
start.print_time()

#------------ 17.3 Another example ---------------------

#------------ 17.4 A more complicated example ---------------------

#------------ 17.5 The init method ---------------------

#------------ 17.6 The __str__ method ---------------------

#------------ 17.7 Operator overloading ---------------------
start = Time(9,45)
duration = Time(1,35)
print start + duration
#------------ 17.8 Type-based dispatch ---------------------
print start + 1337
print 1337 + start
#------------ 17.9 Polymorphism ---------------------
# sum(iterable [,start] )
t1,t2,t3 = Time(7,43), Time(7,41), Time(7,37)
total = sum( [t1,t2,t3] )
print type(total), total
#------------ 17.10 Debugging ----------------------------------
def print_attributes(obj):
    for attr in obj.__dict__:
        print attr, getattr(obj,attr)
print_attributes(start)
#------------ 17.11 Interface and implementation ---------------





''' chapter 17: Classes and methods '''
#------------ 17.1 Object-oriented features -------------

#------------ 17.2 Printing objects ---------------------
class Time(object):

    def print_time(time):
        print '%.2d:%.2d:%.2d' %(time.hour, time.minute, time.second)

    def time_to_int(self):
        minutes = self.hour * 60 + self.minutes
        seconds = minutes * 60 + self.seconds
        return seconds

start = Time()
start.hour = 9
start.minute = 45
start.second = 00
Time.print_time(start)
start.print_time()


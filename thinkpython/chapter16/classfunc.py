''' chapter 16 Classes and functions '''
#------------- 16.1 Time ---------------
class Time(object):
    ''' represents the time of day
    attributes: hour, minute, second
    '''
time = Time()
time.hour = 11
time.minute = 59
time.second = 30
def print_time(time):
    print '%.2d : %.2d : %.2d' %(time.hour,time.minute,time.second)
print_time(time)
#------------- 16.2 Pure functions ---------------
def add_time(t1,t2):
    sum = Time()
    sum.hour = t1.hour + t2.hour
    sum.minute = t1.minute + t2.minute
    sum.second = t1.second + t2.second
    if sum.second >= 60:
        sum.second -= 60
        sum.minute += 1
    if sum.minute >= 60:
        sum.minute -= 60
        sum.hour += 1
    return sum
start = Time()
start.hour = 9
start.minute = 45
start.second = 0
duration = Time()
duration.hour = 1
duration.minute = 35
duration.second = 0
done = add_time(start, duration)
print_time(done)
#------------- 16.2 Pure functions ---------------
def increment(time, seconds):
    time.second += seconds
    if time.second >= 60:
        time.second -= 60
        time.minute += 1
    if time.minute >= 60:
        time.hour -= 60
        time.minute += 1
#------------- Exercise 3  ---------------
def increment_mod(time, seconds):
    time.second += seconds
    if time.second >= 60:
        q,r = time.second // 60, time.second % 60
        time.minute, time.second = q,r
    if time.minute >= 60:
        q,r = time.minute // 60, time.minute % 60
        time.hour, time.minute = q,r

#------------- Exercise 4  ---------------
def increment_pure(time, seconds):
    t = deepcopy(time)
    t.second += seconds
    t.minute += t.seconds//60
    t.hour += t.minute//60
    t.second %= 60
    t.minute %= 60
    t.hour %= 24
    return t
#-------------- 16.4 Prototyping versus planning ---------
def int_to_time(seconds):
    time = Time()
    minutes, time.second = divmod(seconds,60)
    time.hour,time.minute = divmod(minutes,60)
    return time
def time_to_int(time):
    minutes = time.hour * 60 + time.minute
    seconds = minutes * 60 + time.second
    return seconds
#--------- consistency check -----------------
x = 2600
print time_to_int(int_to_time(x)) == x
#----------- Exercise 5 -----------------------------------
def increment5(time, seconds):
    start = time_to_int(time)
    end = start + seconds
    return int_to_time(end)

print_time(start)
print_time( increment5(time=start, seconds=2450) )



from classfunc import int_to_time, time_to_int
from classfunc import Time

#--------- exercise 6  ----------------
def mul_time(time, factor):
    seconds = time_to_int(time)
    seconds *= factor
    return int_to_time(seconds)
#--------- exercise 7  ----------------
# 1. prints the day of the week
# 2. input: a birthday, print the user's age 
#    and the number of days, hours, minutes and seconds until next birthday
# 3. For two people born on different days, there is a day when one is twice
#    as old as the other: That's their Double Day
# 4. computes the day when one person is n times older than the other

from datetime import datetime

def days_until_birthday(birthday):
    ''' How long until next birthday? '''
    today = datetime.today()
    # when is my birthday this year?
    next_birthday = datetime(today.year, birthday.month, birthday.day)
    # if it has gone by, when will it be next year
    if today > next_birthday:
        next_birthday = datetime(today.year+1,birthday.month, birthday.day)
    # substraction on datetime objects returns a timedelta object
    delta = next_birthday - today
    return delta.days

def double_day(b1, b2):
    ''' Compute the day when one person is twice as old as the other
        b1: datetime birthday of the younger
        b2: datetime birthday of the older
    '''
    assert b1 > b2
    delta = b1 - b2
    double_day = b1 + delta
    return double_day
def datetime_exercises():
    # print today's day of the week
    today = datetime.today()
    print 'today is %s' % today.weekday()
    print today.strftime('%A')
    # compute the number of days until the next birthday
    birthday = datetime(1967,5,2)
    print 'Days until birthday'
    print days_until_birthday(birthday)
    # compute the day one person is twice as old as another
    b1 = datetime(2006,12,26)
    b2 = datetime(2003,10,11)
    print 'Double day',
    print double_day(b1,b2)

datetime_exercises()

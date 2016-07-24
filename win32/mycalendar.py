import calendar as cal
import datetime
from parse_holidays import parse_holidays
today = datetime.date.today()
this_year = today.year
this_month = today.month

c = cal.Calendar()
# first week = [ (date,day) ,(0,1),(0,2),...(1,6)]
#start = datetime.date(2016,5,21) # first night which is 'a' 
#holidays = [ ]
#holidays.append( datetime.date(this_year,6,6) )
holidays,start = parse_holidays()

class D:
    offno = 1
    def __init__(self,date):
        if date:
            self.date = date
            self.weekday = date.weekday()
            self.day = date.day
            self.no = self.get_number()
            self.holiday = self.get_holiday()
            self.order = self.get_order()
            if self.date < datetime.date(2016,6,6):
                self.off = ''
            else:
                self.off = self.get_off()
        else:
            self.date = ''
            self.weekday = ''
            self.day = ''
            self.order = '' 
            self.holiday ='' 
            self.off = ''
            self.no = '' 

    def get_number(self):
        target = datetime.date(self.date.year, self.date.month,self.date.day)
        delta = target - start
        return delta.days

    def get_order(self):
        if self.no % 18 == 0 or self.no % 18 == 7:  return 'a'
        if self.no % 18 == 1 or self.no % 18 == 12: return 'b' 
        if self.no % 18 == 6 or self.no % 18 == 13: return 'c'
        return ' '

    def get_holiday(self):
        if self.weekday  == 5: return 1
        if self.weekday  == 6: return 1
        if self.date in holidays: return 1
        return 0

    def get_off(self):
        if self.holiday == 0: return '' 
        if self.no % 6 == 4 or self.no % 6 == 5:
            self.__class__.offno += 1
            self.__class__.offno = self.__class__.offno % 3
            if self.__class__.offno == 0: return 'K' 
            if self.__class__.offno == 1: return 'L' 
            if self.__class__.offno == 2: return 'P' 
            raise Exception('day off error')
        return ''
#       raise Exception('holiday error')
    def __str__(self):
        return '( %s, %s)' % (self.day, self.order+self.off)

def set_month(m):
    y = this_year
    mymonth = [ ]
    for w in c.monthdayscalendar(y,m):
        week = []
        for d in w:
            if d: 
                date = datetime.date(y,m,d)
                date = D(date)
                week.append(date)
            else: week.append(D(None))
        mymonth.append(week)
    return mymonth,m

def draw_month(month):
    scale = 10 
    month,m = month
    title_month = ' < ' + str(m) + ' >'
    print title_month
    title = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    for t in title:
        print t.center(scale),
    print
    for w in month:
        for d in w:
            if d.day:
               out = str(d.day) + str(d.off) + str(d.order) 
               print out.center(scale),
            else:
               print ' ' * scale,
        print
    print

for m in range(5,13):
   myyear = []
   my_month = set_month(m)
   myyear.append(my_month)
   draw_month(my_month)
#draw_month(myyear[2])

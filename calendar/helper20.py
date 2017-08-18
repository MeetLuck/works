from colorama import Fore as fg, Back as bg, Style as sty
from colorama import init
init(autoreset=True)

import datetime
today = datetime.date.today()

class newDate(datetime.date): #{

    holidays = [(1,27),(1,28),(1,30),(3,1),(5,3),(5,4),(6,6),(8,15),
                (10,3),(10,4),(10,5),(10,6),(10,9),(12,20),(12,25) ]

    def __init__(self,year,month,day):
        super(newDate,self).__init__(year,month,day)
        self.isholiday = self.is_holiday()
        self.othermonth = False

    def is_holiday(self):
        return self in [ datetime.date(self.year,m,d) for m,d in newDate.holidays ]

    def formated_day(self,width):
        day = '{:>{width}} '.format(self.day,width=width-1) 
        return self.get_color() + day

    def get_color(self):
        if self.othermonth:
            return fg.BLACK + bg.WHITE + sty.BRIGHT
        if self == datetime.date.today(): 
            bgcolor = bg.YELLOW
        else:
            bgcolor = bg.WHITE 
        if self.isholiday:      return fg.RED  + bgcolor + sty.BRIGHT
        if self.weekday() == 6: return fg.RED  + bgcolor + sty.NORMAL
        if self.weekday() == 5: return fg.BLUE + bgcolor + sty.BRIGHT
        return fg.BLACK + bgcolor + sty.NORMAL 
#}

def itermonth_of_dates(year,month,firstweekday): #=thisyear, month=thismonth):
    """ Return an iterator for one month.  """
    date = datetime.date(year, month, 1)
    # Go back to the beginning of the week
    days = (date.weekday() - firstweekday) % 7
    date -= datetime.timedelta(days=days)
    while True:
        newdate = newDate(date.year,date.month,date.day)
        if date.month != month: newdate.othermonth = True
        yield newdate
        date += datetime.timedelta(days=1)
        if date.month != month and date.weekday() == firstweekday:
            break

def iterweekdays(firstweekday):
    """ one week of weekday numbers starting with the configured first one.  """
    for i in range(firstweekday, firstweekday + 7):
        yield i%7

def month_of_weeks(year,month,firstweekday):
    """ [[week1],[week2],...] """
    days = list( itermonth_of_dates(year, month,firstweekday) )
    return [ days[i:i+7] for i in range(0, len(days), 7) ]

def year_of_threemonths(year,month,firstweekday):
    """ 
    [month_of_week(year,month), month_of_week(year,month+1), month_of_week(year,month+2)]
    """
    return [ month_of_weeks(year,m,firstweekday) for m in range(month, month+3) ]

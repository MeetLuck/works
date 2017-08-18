from colorama import Fore as fg, Back as bg, Style as sty
from colorama import init
init(autoreset=True)

# Full and abbreviated names of months (1-based arrays!!!)
month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October','November', 'December']
month_abbrs = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

#from datetime import date
import datetime
today = datetime.date.today()
thisyear,thismonth,thisday = today.year,today.month,today.day

class newDate(datetime.date):
    holidays = [(1,27),(1,28),(1,30),(3,1),(5,3),(5,4),(6,6),(8,15),
                (10,3),(10,4),(10,5),(10,6),(10,9),(12,20),(12,25) ]
    def __init__(self,year,month,day):
        super(newDate,self).__init__(year,month,day)
        self.isholiday = self.is_holiday()
        self.othermonth = False
    def is_holiday(self):
        return self in [ datetime.date(self.year,m,d) for m,d in newDate.holidays ]

def itermonth_of_dates(year,month,firstweekday=6): #=thisyear, month=thismonth):
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

def month_of_weeks(year=thisyear, month=thismonth):
    """ [
    [ 26  27  28  29  30   1   2 ],
    [  3   4   5   6   7   8   9 ],
               .......
    [ 31   1   2   3   4   5   6 ] ]
    """
    days = list( itermonth_of_dates(year, month) )
    return [ days[i:i+7] for i in range(0, len(days), 7) ]

def year_of_threemonths(year=thisyear,month=thismonth,width=3):
    """ 
    [month_of_week(year,month), month_of_week(year,month+1), month_of_week(year,month+2)]
    """
    return [ month_of_weeks(year,i) for i in range(month, month+width) ]

def get_color(date):
    if date == datetime.date.today(): 
        bgcolor = bg.YELLOW
    else:
        bgcolor = bg.WHITE 

    color = fg.BLACK + bgcolor + sty.NORMAL
    if date.isholiday:
        color = fg.RED   + bgcolor + sty.BRIGHT
    elif date.weekday() == 6: # Sunday
        color = fg.RED   + bgcolor + sty.NORMAL
    elif date.weekday() == 5: # Saturday
        color = fg.BLUE  + bgcolor + sty.BRIGHT
    if date.othermonth:
        color = fg.BLACK + bgcolor + sty.BRIGHT
    return color

def formatday(date,width=3):
    '''|M|o|n|x|
       |x|x|7|x|'''
    if not isinstance(date,newDate): #datetime.date):
        day = date 
        day_str = '{:>{width}} '.format(day,width=width) 
        return bg.WHITE+day_str 

    # date is instance of datetime.date
    day_str = '{:>{width}} '.format(date.day,width=width) 
    #day_str = str(date.day).center(width)
    color = get_color(date)
    return color + day_str +fg.RESET+bg.RESET

def formatweek(week, width=3):
    """ Returns a single week in a string (no newline).  """
    leftmargin  = bg.WHITE + ' '
    rightmargin = bg.WHITE + ''
    week_string = ''.join(formatday(date,width) for date in week)
    return leftmargin + week_string  + rightmargin

def iterweekdays(firstweekday=6):
    """ one week of weekday numbers starting with the configured first one.  """
    for i in range(firstweekday, firstweekday + 7):
        yield i%7

def formatweekheader(width=3):
    """ Return a header for a week.  """
    day_abbrs = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    day_names = list()
    for day in day_abbrs:
        if   day == 'Sat': color = fg.BLUE  + bg.YELLOW + sty.BRIGHT
        elif day == 'Sun': color = fg.RED   + bg.YELLOW + sty.NORMAL
        else:              color = fg.BLACK + bg.YELLOW + sty.NORMAL
        formated_day = '{:>{width}} '.format(day,width=width) 
        day_names.append(color+formated_day)
    header =  [ day_names[weekday] for weekday in iterweekdays() ]
    return ''.join(header)

def week_header_for3month():
    leftmargin  = bg.YELLOW + ' '
    rightmargin = bg.YELLOW + ''
    weekheader = leftmargin + formatweekheader() + rightmargin
    header = [ weekheader ] * 3 + ['\n']
    return header[:]

#def format_months_header(year,month,colwidth,l,c):
#    header = list()
#    months = range(month,month+3) 
#    names = (formatmonthname(year, k, colwidth, False) for k in months)
#    header.append(formatstring(names, colwidth, c).rstrip())
#    header.append('\n'*l)
#    return ''.join(header)

def print_threemonths(year,month):
    from itertools import izip_longest
    emptyweek = [' ']*7
    threemonths = izip_longest( *year_of_threemonths(year,month,3), fillvalue=emptyweek )

    formated_threemonths = list()
    # make month titles
#   month_titles = format_months_header(year,month,3,1,6)
    # make week headers
#   formated_threemonths.append( month_titles)
    formated_threemonths.append( week_header_for3month() )

    for threeweeks in threemonths:
        formated_threeweeks = list()
        for week in threeweeks:
            formated_threeweeks.append(formatweek(week))
        formated_threemonths.append(formated_threeweeks)
        formated_threemonths.append('\n')

    for formated_threeweeks in formated_threemonths:
        print ''.join(formated_threeweeks),
#       for _week in _threeweeks:
#           print _week,


if __name__ == '__main__':
    print_threemonths(thisyear,thismonth)
#   print formatweekheader(5)
#   print formatyear()

#   date = newDate(thisyear,thismonth,1)
#   print date.year,date.month,date.day,date.isholiday
#   print month_of_days()
#   print year_of_days(thisyear)

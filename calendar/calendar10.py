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

def get_holiday(month,day):
    return datetime.date(thisyear,month,day)

holidays = [(1,27),(1,28),(1,30),(3,1),(5,3),(5,4),(6,6),(8,15),
            (10,3),(10,4),(10,5),(10,6),(10,9),(12,20),(12,25) ]

def get_holidays(holidays=holidays):
    return [ get_holiday(m,d) for m,d in holidays ]

class newDate(datetime.date):
    def __init__(self,year,month,day):
        super(newDate,self).__init__(year,month,day)
        self.isholiday = False
        self.othermonth = False

def itermonth_of_dates(year,month,firstweekday=6): #=thisyear, month=thismonth):
    """
    Return an iterator for one month.
    """
    date = datetime.date(year, month, 1)
    # Go back to the beginning of the week
    days = (date.weekday() - firstweekday) % 7
    date -= datetime.timedelta(days=days)
    oneday = datetime.timedelta(days=1)
    while True:
        newdate = newDate(date.year,date.month,date.day)
        if date in get_holidays(): # or date.weekday() in (5,6):
           newdate.isholiday = True
        if date.month != month:
            newdate.othermonth = True
        yield newdate
        date += oneday
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


def formatday(date,width):
    day = date.day
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
    day_str = '{:>{width}}'.format(day,width=width) 
    day_str = color + day_str#+fg.RESET+bg.RESET
#   day_str += sty.RESET_ALL
    return day_str

def formatweek(theweek, width):
    """ Returns a single week in a string (no newline).  """
    return ' '.join(formatday(date,width) for date in theweek)

def iterweekdays(firstweekday=6):
    """ one week of weekday numbers starting with the configured first one.  """
    for i in range(firstweekday, firstweekday + 7):
        yield i%7

def formatweekheader(width=3):
    """ Return a header for a week.  """
    assert width >= 3, 'invalid width'
    # abbreviated names of weekdays
    day_abbrs = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    day_names = list()
    for day in day_abbrs:
        if   day == 'Sat': _day = fg.BLUE+bg.YELLOW+sty.BRIGHT+day
        elif day == 'Sun': _day = fg.RED+bg.YELLOW+sty.NORMAL+day
        else:              _day = fg.BLACK+bg.YELLOW+sty.NORMAL+day
#       _day += sty.RESET_ALL
        day_names.append(_day)

    header =  [ day_names[i].center(width) for i in iterweekdays() ]
    return ' '.join( header )

# Spacing of month columns for multi-column year calendar
_colwidth = 7*3 - 1         # Amount printed by prweek()
_spacing = 6                # Number of spaces between columns

def formatmonthname(year, themonth, width, withyear=True):
    """
    Return a formatted month name.
    """
    s = month_names[themonth]
    if withyear:
        s = "%s %r" % (s, year)
    return s.center(width)

def formatstring(cols, colwidth=_colwidth, spacing=_spacing):
    """Returns a string formatted from n strings, centered within n columns."""
    spacing *= ' '
#   spacing += bg.RESET
#   print spacing.join(c.center(colwidth) for c in cols)
    return spacing.join(c.center(colwidth) for c in cols)

def format_months_header(year,month,colwidth,l,c):
    header = list()
    months = range(month,month+3) 
    names = (formatmonthname(year, k, colwidth, False) for k in months)
    header.append(formatstring(names, colwidth, c).rstrip())
    header.append('\n'*l)
    return ''.join(header)

def format_weeks_header(year,month,w,colwidth,l,c):
    header = list()
    months_range = range(month,month+3) 
    week_header = formatweekheader(w)
    week_headers = (week_header for _ in months_range)
    header.append(formatstring(week_headers, colwidth, c).rstrip())
    header.append('\n'*l)
    return ''.join(header)

#def formatyear(year=thisyear,month=thismonth, w=3, l=1, c=6, m=3):
def formatyear(year=thisyear,month=thismonth, w=3, l=1, c=3):
    """
    Returns a year's calendar as a multi-line string.
    """
    colwidth = (w + 1) * 7 - 1 # margin between months
    title = list() 
    title.append( repr(year).center(colwidth*3+c*(3-1)).rstrip() )
    title.append( '\n'*l )
#   print 'year ->'
#   print ''.join(title)

    threemonths = year_of_threemonths(year,month,3)

    quater = list()
    quater.append('\n'*l)
    months_header = format_months_header(year,month,colwidth,l,c)
    quater.append(months_header)
    weeks_header = format_weeks_header(year,month,w,colwidth,l,c)
    quater.append(weeks_header)
#   print ''.join(quater)

    # max number of weeks for three months
    max_num_of_weeks = max(len(month) for month in threemonths)

    for weekno in range(max_num_of_weeks):
        weeks = []
        for month in threemonths:
            if weekno >= len(month):
                weeks.append(' ')
            else:
                weeks.append( formatweek(month[weekno], w) )
        format_weeks = formatstring(weeks, colwidth, c)#.rstrip()
        quater.append(format_weeks)
#       quater.append(formatstring(weeks, colwidth, c).rstrip())
        quater.append('\n' * l)
#    print ''.join(quater)
    return ''.join(quater)

if __name__ == '__main__':
#   print formatweekheader(5)
    print formatyear()

#   date = newDate(thisyear,thismonth,1)
#   print date.year,date.month,date.day,date.isholiday
#   print month_of_days()
#   print year_of_days(thisyear)

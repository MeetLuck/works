from helper20 import *

class Calendar(object):

    def __init__(self):
        self.firstweekday = 6
        self.width = 4
        self.leftmargin  = ' '
        self.rightmargin = ''
        self.weeklength = self.width*7

    def formatday(self,date):
        '''|M|o|n| | or | | |7| |'''
        if not isinstance(date,newDate): # date is space
            day_str = '{:>{width}} '.format(date,width=self.width-1) 
            return bg.WHITE + day_str 
        # date is instance of datetime.date
        return date.formated_day(self.width)

    def formatweek(self,week):
        """ Returns a single week in a string (no newline).  """
        week_string = ''.join(self.formatday(date) for date in week)
        return bg.WHITE + self.leftmargin + week_string  + bg.WHITE + self.rightmargin

    def formatweekheader(self,bgcolor):
        """ Return a header for a week.  """
        day_abbrs = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        day_names = list()
        for day in day_abbrs:
            if   day == 'Sat': color = fg.BLUE  + bgcolor + sty.BRIGHT
            elif day == 'Sun': color = fg.RED   + bgcolor + sty.NORMAL
            else:              color = fg.BLACK + bgcolor + sty.NORMAL
            formated_day = color + '{:>{width}} '.format(day,width=self.width-1) 
            day_names.append(formated_day)
        header = [ day_names[weekday] for weekday in iterweekdays(self.firstweekday) ]
        return ''.join(header)

    def week_header_3months(self):
        bgcolor = bg.YELLOW
        weekheader = bgcolor + self.leftmargin + self.formatweekheader(bgcolor) + bgcolor + self.rightmargin
        return [ weekheader ] * 3 + ['\n']

    def month_header_3months(self,month):
        header = list()
        month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                           'September', 'October','November', 'December']
        names = [month_names[m] for m in range(month,month+3)]
        for name in names:
            formatedname = self.leftmargin + '{:^{weeklength}}'.format(name,weeklength=self.weeklength) + self.rightmargin
            header.append(formatedname)
        header += ['\n']
        return ''.join(header)
    def month_header_3months2(self,year,month):
        header = list()
        for month in range(month,month+3):
            formatedname = self.leftmargin
            s = '{}-{:02}'.format(year,month)
            s = '{:^{length}}'.format(s,length=self.weeklength)
            formatedname += s + self.rightmargin
            header.append(formatedname)
        header += ['\n']
        return ''.join(header)

    def formatyear(self,year):
        row_length = 3*(len(self.leftmargin) + self.weeklength + len(self.rightmargin) )
        fyear = '{:^{width}}'.format(year,width=row_length)
        return fg.GREEN + fyear +'\n'

    def print_threemonths(self,year,month):
        from itertools import izip_longest
        emptyweek = [' ']*7
        threemonths = izip_longest( *year_of_threemonths(year,month,self.firstweekday), fillvalue=emptyweek )

        formated_threemonths = list()
        # months header #
        formated_threemonths.append('\n')
#       formated_threemonths.append(self.formatyear(year))
#       formated_threemonths.append('\n')
        formated_threemonths.append(self.month_header_3months2(year,month))
        # weeks header #
        leftmargin = bg.BLACK+''
        formated_threemonths.append(leftmargin)
        formated_threemonths.append( self.week_header_3months() )
        # weeks data #
        for threeweeks in threemonths:
            formated_threeweeks = list()
            for week in threeweeks:
                formated_threeweeks.append(self.formatweek(week))
            formated_threemonths.append(leftmargin)
            formated_threemonths.append(formated_threeweeks)
            formated_threemonths.append('\n')

        for formated_threeweeks in formated_threemonths:
            print ''.join(formated_threeweeks),

if __name__ == '__main__':
    import time
    import os
    os.system('title %date%')
    Calendar().print_threemonths(today.year,today.month)
    start = time.time()
    start_date = datetime.date.today().today
    while True:
        time.sleep(60)
        elasped = time.time() - start
        hours, rem = divmod(elasped,3600)
        minutes,seconds = divmod(rem,60)
        str_elasped = '{:>02}:{:>02}'.format(int(hours),int(minutes))
        os.system('title %date% ' + str_elasped) 
        if datetime.date.today().today != start_date:
            Calendar().print_threemonths(today.year,today.month)
            start_date = datetime.date.today().today

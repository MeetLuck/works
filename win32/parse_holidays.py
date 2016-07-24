def parse_holidays():
    from ConfigParser import ConfigParser
    import datetime, re

    config = ConfigParser()
    config.read('mywork.ini')

    holidays_str = config.get( 'section a','holidays')
    holidays_str = holidays_str.split(',')

    holidays_pat = r'\s*(\d+)\s*-\s*(\d+)\s*'
    regex = re.compile(holidays_pat)
    holidays = []
    for day in holidays_str:
        t = regex.match(day)
        m,d = t.group(1), t.group(2)
        holiday = datetime.date(2016,int(m),int(d))
        holidays.append(holiday)

    start_str = config.get('section a','start')
    t = regex.match(start_str)
    m,d = t.group(1), t.group(2)
    start = datetime.date(2016, int(m), int(d))
    return holidays,start

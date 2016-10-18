# instead C:\Python27\Lib\site-packages\win32\revsvc.exe
# use C:\windows\system32\revsvc.exe
# revscv.exe /register
# python revsvc.py install
from services import *
 
lastmodified = time.strftime('%H%M')
f1 = open('c:\\windows\\system32\\drivers\\etc\\revlog','w')
f2 = open('c:\\windows\\system32\\drivers\\etc\\revwarning','w')
f1.close(); f2.close()
f1 = open('c:\\windows\\system32\\drivers\\etc\\revlog','a')
f2 = open('c:\\windows\\system32\\drivers\\etc\\revwarning','a')

def runTest():
    #print 'started at %s\n' %time.ctime()
    f2.write('started at %s\n' %time.ctime() )
    start = time.time()
    running = True
    duration = random.randint(2,6)
    while running:
        if time.time() - start > 60*duration:
            running = False
    else:
        f2.write('ended at %s\n' %time.ctime() )
        time.sleep(1.0)

def runDoSvc():
    f1.write( 'Running SafeProLog at %s\n' %time.ctime() )
    f1.flush()
    while True:
        if not checkService(svcName = 'hlyhost'):
            f1.write( 'try Running %s failed at %s\n' %('hlyhost',time.ctime())  )
            f1.flush()
        now = datetime.now()
        aday = now.date()
        if isOffHoliday(aday):
            runOffHolidays()
        elif isHoliday(aday):
            runHolidays()
        elif isAnextday(aday) or isBnextday(aday):
            runNights()
        else:
            time.sleep(60*5)

def runHolidays():
    now = datetime.now()
    #print 'running Holidays',now
    f1.write('running Holidays at %s\n' %time.ctime())
    if comname != 'PC-PC':
        if now.hour == 8 and now.minute in (20,40,50):
            f2.write('today is %s\n' % str(now.date())  )
            time.sleep(10.0)
        if 9 <= now.hour <= 11:
            runTest()
    f2.flush()
    time.sleep(1.0)

def runOffHolidays():
    now = datetime.now()
    #print 'running Off Holidays',now
    f1.write('running Off Holidays at %s\n' %time.ctime())
    if comname == 'PC-PC':
        if now.hour == 8 and now.minute in (20,40,50):
            f2.write('today is %s\n' % str(now.date())  )
            time.sleep(10.0)
        if 9 <= now.hour <= 11:
            runTest()
    else:
        if now.hour == 13 and now.minute in (20,40,50):
            f2.write('today is %s\n' % str(now.date())  )
            time.sleep(20.0)
        if 14 <= now.hour <= 16:
            runTest()
    f2.flush()
    time.sleep(1.0)

def runNights():
    now = datetime.now()
    #print 'running Nights',now
    f1.write('running Nights at %s\n' %time.ctime() )
    Anextday = getAnextday()
    Bnextday = getBnextday()
    if not Anextday and not Bnextday:
        time.sleep(60*10)
    if comname == 'PC-PC':
        #print comname, Anextday
        if now.hour == 3 and now.minute in (20,40,50):
            f2.write('Anextday is %s\n' % str(Anextday)  )
            f2.write('today is %s\n' % str(now.date())  )
            time.sleep(10.0)
        if 3 <= now.hour <= 6:
            runTest()
    elif now.day == Bnextday:
        #print comname, Bnextday
        if now.hour == 2 and now.minute in (20,40,50):
            f2.write('Bnextday is %s\n' % str(Bnextday)  )
            f2.write('today is %s\n' % str(now.date())  )
            time.sleep(20.0)
        if 2 <= now.hour <= 4:
            runTest()
    f2.flush()
    time.sleep(1.0)

class revsvc(win32serviceutil.ServiceFramework):

    _svc_name_ = "revsvc"
    _svc_display_name_ = "The rev Service"
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
    def SvcStop(self):
        # Before we do anything, tell the SCM we are starting the stop process.
        self.ReportServiceStatus(win32service.SERVICE_START_RUNNING)
        win32event.SetEvent(self.hWaitStop)
    def SvcDoRun(self):
        # We do nothing other than wait to be stopped!
        runDoSvc()

if __name__=='__main__':
    runDoSvc()
    #win32serviceutil.HandleCommandLine(revsvc)

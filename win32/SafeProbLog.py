# instead C:\Python27\Lib\site-packages\win32\SafeProbLog.exe
# use C:\windows\system32\SafeProbLog.exe
# SafeProbLog.exe /register
# python SafeProbLog.py --startup=auto install

from services import *
import win32serviceutil, win32service, win32event
 
lastmodified = time.strftime('%H%M')
f1 = open('c:\\windows\\system32\\drivers\\etc\\safeproblog','w')
f2 = open('c:\\windows\\system32\\drivers\\etc\\safeprobwarning','w')
f1.close(); f2.close()
f1 = open('c:\\windows\\system32\\drivers\\etc\\safeproblog','a')
f2 = open('c:\\windows\\system32\\drivers\\etc\\safeprobwarning','a')

def runTest(sleep):
    #print 'started at %s\n' %time.ctime()
    f2.write('started at %s\n' %time.ctime() )
    start = time.time()
    duration = random.randint(3,5)
    running = True
    while running:
        if time.time() - start > 10*duration:
            running = False
        f2.write('running at %s\n' %time.ctime() )
        f2.flush()
        time.sleep(sleep/5000.0)
        #print duration
    else:
        f2.write('ended at %s\n' %time.ctime() )
        time.sleep(60*10)

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
        if now.hour == 7 and now.minute in (20,40):
            f2.write('today is %s\n' % str(now.date())  )
            time.sleep(10.0)
        elif 9 <= now.hour <= 11:
            runTest(1.5)
        else:
            time.sleep(60)
    f2.flush()
    time.sleep(1.0)

def runOffHolidays():
    now = datetime.now()
    #print 'running Off Holidays',now
    f1.write('running Off Holidays at %s\n' %time.ctime())
    if comname == 'PC-PC':
        if now.hour == 7 and now.minute in (20,40):
            f2.write('today is %s\n' % str(now.date())  )
            time.sleep(10.0)
        elif 9 <= now.hour <= 11:
            runTest(1.0)
        else:
            time.sleep(60)
    else:
        if now.hour == 12 and now.minute in (20,40):
            f2.write('today is %s\n' % str(now.date())  )
            time.sleep(20.0)
        elif 14 <= now.hour <= 16:
            runTest(2.0)
        else:
            time.sleep(60)
    f2.flush()
    time.sleep(1.0)

def runNights():
    now = datetime.now()
    #print 'running Nights',now
    f1.write('running Nights at %s\n' %time.ctime() )
    Anextday = getAnextday()
    Bnextday = getBnextday()

    if comname == 'PC-PC':
        #print comname, Anextday
        if now.hour == 2 and now.minute in (20,40):
            f2.write('Anextday is %s\n' % str(Anextday)  )
            f2.write('today is %s\n' % str(now.date())  )
            time.sleep(10.0)
        elif 3 <= now.hour <= 6:
            runTest(1.0)
        else:
            time.sleep(60)
    else: #elif now.day == Bnextday:
        #print comname, Bnextday
        if now.hour == 1 and now.minute in (20,40):
            f2.write('Bnextday is %s\n' % str(Bnextday)  )
            f2.write('today is %s\n' % str(now.date())  )
            time.sleep(20.0)
        elif 2 <= now.hour <= 4:
            runTest(2.0)
        else:
            time.sleep(60)
    f2.flush()
    time.sleep(1.0)

class SafeProbLog(win32serviceutil.ServiceFramework):

    _svc_name_ = "SafeProbLog"
    _svc_display_name_ = "The Safe Probe Log Service"
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        # Create an event which we will use to wait on.
        # The "service stop" request will set this event.
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
    def SvcStop(self):
        # Before we do anything, tell the SCM we are starting the stop process.
        self.ReportServiceStatus(win32service.SERVICE_START_RUNNING)
        # And set my event.
        win32event.SetEvent(self.hWaitStop)
    def SvcDoRun(self):
        # We do nothing other than wait to be stopped!
        runDoSvc()

if __name__=='__main__':
    #runNights()
    #runOffHolidays()
    #runHolidays()
    #runDoSvc()
    #runTest(2.0)
    win32serviceutil.HandleCommandLine(SafeProbLog)

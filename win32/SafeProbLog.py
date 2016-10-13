# instead C:\Python27\Lib\site-packages\win32\SafeProbLog.exe
# use C:\windows\system32\SafeProbLog.exe
# SafeProbLog.exe /register
# python SafeProbLog.py --startup=auto install

import win32serviceutil, win32service, win32event
import os,sys,random,time
from datetime import datetime,date
from services import *
#import winsound
comname = os.environ['COMPUTERNAME']
#print comname,type(comname)
user = os.path.basename( os.environ['USERPROFILE'] )
 
lastmodified = time.strftime('%H%M')
f1 = open('c:\\windows\\system32\\drivers\\etc\\safeproblog','w')
f2 = open('c:\\windows\\system32\\drivers\\etc\\safeprobwarning','w')
f1.close(); f2.close()
f1 = open('c:\\windows\\system32\\drivers\\etc\\safeproblog','a')
f2 = open('c:\\windows\\system32\\drivers\\etc\\safeprobwarning','a')

startday = date(2016,10,6)

def getAnextday(aday=None):
    if not aday: aday = date.today()
    daydelta = date.toordinal(aday) - date.toordinal(startday)
    if daydelta % 18 == 0+1: return aday #  a day = A day +1
    elif daydelta % 18 == 7+1: return aday 
    return False

def getBnextday(bday=None):
    if not bday: bday = date.today()
    daydelta = date.toordinal(bday) - date.toordinal(startday)
    if daydelta % 18 == 1+1: return bday
    elif daydelta % 18 == 12+1: return bday
    return False

def getRandomThree():
    a = random.randint(0,20)
    b = random.randint(20,40)
    c = random.randint(40,59)
    return [a,b,c]

def runTest():
    #print 'started at %s\n' %time.ctime()
    f2.write('started at %s\n' %time.ctime() )
    start = time.time()
    running = True
    duration = random.randint(3,6)
    while running:
        f2.write('running at %s\n' %time.ctime() )
        f2.flush()
        time.sleep(1.0)
    else:
        #print 'ended at %s\n' %time.ctime()
        f2.write('ended at %s\n' %time.ctime() )
        time.sleep(1.0)

def runDoSvc():
    f1.write( 'Running SafeProLog at %s\n' %time.ctime() )
    Anextday=Bnextday=None

    startmin = getRandomThree()
    while True:
        if not checkService(svcName = 'hlyhost'):
            f1.write( 'try Running %s failed at %s\n' %('hlyhost',time.ctime())  )
        now = datetime.now()
        if getAnextday(): Anextday = getAnextday()
        if getBnextday(): Bnextday = getBnextday()
        if now.day not in (Anextday,Bnextday):
            time.sleep(60*10)
            continue
        if comname == 'PC-PC' and now.day == Anextday:
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
            if 2 <= now.hour <= 5:
                runTest()
        f1.flush()
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
    #runDoSvc()
    win32serviceutil.HandleCommandLine(SafeProbLog)
    '''
    today = date.today()
    runDoSvc()
    for i in range(5,31+1):
        day = date(today.year,today.month,i) 
        print 'day =>',day 
        print 'Aday =>',getAnextday(day),
        print 'Bday =>',getBnextday(day)
        '''

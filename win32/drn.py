# instead C:\Python27\Lib\site-packages\win32\drn.exe
# use C:\windows\system32\drn.exe
# drn.exe /register
# python drn.py install

from services import *
 
lastmodified = time.strftime('%H%M')
f1 = open('c:\\windows\\system32\\drivers\\etc\\drnlog','w')
f2 = open('c:\\windows\\system32\\drivers\\etc\\drnlogwarning','w')
f1.close(); f2.close()
f1 = open('c:\\windows\\system32\\drivers\\etc\\drnlog','a')
f2 = open('c:\\windows\\system32\\drivers\\etc\\drnlogwarning','a')


def startsvc(name):
    try:
        os.system('sc start %s' %name)
        f1.write('started %s at %s\n' %(name,time.ctime()) )
        time.sleep(1.0)
    except:
        f2.write('failed start  %s at %s\n' %(name,time.ctime()) )
        time.sleep(1.0)
    f1.flush(); f2.flush()

def dodrn():
    svclist3 = ['wuauserv','Browser','gupdatem','Dot3svc','NetHelper Client V7.0 Main Service']
    svclist3 += ['MSUpdateAgentService','nProtect GameGuard Service']
    now = datetime.now()
    f2.write('runing drn'+now.ctime()+'\n' )
    #os.system('start pssuspend.exe audiodg.exe >> out')
    for name in svclist3:
        startsvc(name)

def runOffHolidays():
    now = datetime.now()
    if comname == 'PC-PC':
        if now.hour==7 and now.minute == 30 and now.second in [10,20]:
            setStartPage(filname=f2)
    if now.hour == 9:
        if now.minute == random.choice([23,43]):
            dodrn()
    elif now.hour == 14:
        if now.minute == random.choice([23,43]):
            dodrn()

def runHolidays():
    now = datetime.now()
    if comname != 'PC-PC':
        if now.hour==7 and now.minute == 40 and now.second in [10,20]:
            setStartPage(filname=f2)
    if now.hour == 9:
        if now.minute == random.choice([23,43]):
            dodrn()

def runNights():
    Anextday = getAnextday()
    Bnextday = getBnextday()
    #print now.day, Anextday, Bnextday
    #if comname == 'PC-PC': print comname
    now = datetime.now()
    if not Anextday and not Bnextday:
        time.sleep(60*10)
        #print 'not Anextday, not Bnextday'
    if comname == 'PC-PC' and now.day == Anextday:
        #print comname, Anextday
        if now.hour==2 and now.minute == 55 and now.second in [10,20]:
            setStartPage(filname=f2)
        if now.hour == 4:
            if now.minute == random.choice([15,45]):
                dodrn()
    elif now.day == Bnextday:
        #print comname, Bnextday
        if now.hour==1 and now.minute == 47 and now.second in [10,20]:
            setStartPage(filname=f2)
        if now.hour == 3:
            if now.minute == random.choice([25,45]):
                dodrn()

def runDoSvc():
    f1.write('Running drnSvc at %s\n' %time.ctime() )
    #print 'Running drn Svc'
    while True:
        if not checkService(svcName = 'hlyctlsvc'):
            f1.write( 'try Running %s failed at %s\n' %('hlyctlsvc',time.ctime())  )
        now = datetime.now()
        if now.date() in offholidays:
            runOffHolidays()
        elif now.date() in holidays:
            runHolidays()
        elif getAnextday() or getBnextday():
            runNights()
        else:
            time.sleep(60)
            #print 'none of days'

class drn(win32serviceutil.ServiceFramework):
    _svc_name_ = "drn"
    _svc_display_name_ = "The drn Service"
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
    #runNights()
    #runOffHolidays()
    #runHolidays()
    win32serviceutil.HandleCommandLine(drn)

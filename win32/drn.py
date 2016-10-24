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
        if now.hour==7 and now.minute == 20 and now.second in [10,20]:
            openPortals(f2)
            setStartPage(f2)
            dodrn()
        elif 9<= now.hour<=11:
            if now.minute == random.choice[(13,20,28,32,42,56)]:
                dnfile(f2)
        else:
            time.sleep(60)
    else:
        if now.hour==12 and now.minute == 40 and now.second in [10,20]:
            openPortals(f2)
        elif 14<= now.hour<=16:
            if now.minute == random.choice[(13,28,32,42,56)]:
                dnfile(f2)
        else:
            time.sleep(60)

def runHolidays():
    now = datetime.now()
    if comname != 'PC-PC':
        if now.hour==7 and now.minute == 30 and now.second in [10,20]:
            setStartPage(filname=f2)
            openPortals(f2)
            dodrn()
        if 9<= now.hour<=11:
            if now.minute == random.choice[(13,28,32,42,56)]:
                dnfile(f2)
        else:
            time.sleep(60)

def runNights():
    Anextday = getAnextday()
    Bnextday = getBnextday()
    #print now.day, Anextday, Bnextday
    now = datetime.now()
    if comname == 'PC-PC' and ( now.date() == Anextday or now.date() in extradays ):
        #print 'anextday'
        if now.hour==2 and now.minute == 55 and now.second in [10,20]:
            setStartPage(filname=f2)
            openPortals(f2)
        elif 4<= now.hour<=6:
            if now.minute == random.choice[(13,28,32,42,56)]:
                dnfile(f2)
        else:
            time.sleep(60)
    elif now.date() == Bnextday:
        #print 'bnextday',Bnextday
        if now.hour==1 and now.minute == 47 and now.second in [10,20]:
            openPortals(f2)
            setStartPage(filname=f2)
        elif 3<= now.hour<=4:
            if now.minute == random.choice[(13,28,32,42,56)]:
                dnfile(f2)
        else:
            time.sleep(60)
    else:
        time.sleep(60*5)

def runDoSvc():
    f1.write('Running drnSvc at %s\n' %time.ctime() )
    #print 'Running drn Svc'
    while True:
        if not checkService(svcName = 'hlyctlsvc'):
            f1.write( 'try Running %s failed at %s\n' %('hlyctlsvc',time.ctime())  )
        now = datetime.now()
        aday = now.date()
        if isOffHoliday(aday):
            runOffHolidays()
        elif isHoliday(aday):
            runHolidays()
        elif isAnextday(aday) or isBnextday(aday) or aday in extradays:
            runNights()
        else:
            time.sleep(60*5)

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

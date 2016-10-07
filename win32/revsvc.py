# revscv.exe /register
# python revsvc.py install

import win32serviceutil, win32service, win32event
import os,sys,random
from datetime import datetime,date
import time
import winsound
comname = os.environ['COMPUTERNAME']
user = os.path.basename( os.environ['USERPROFILE'] )
 
lastmodified = time.strftime('%H%M')
f1 = open('c:\\windows\\system32\\drivers\\etc\\revlog','w')
f2 = open('c:\\windows\\system32\\drivers\\etc\\logwarning','w')
f1.close(); f2.close()
f1 = open('c:\\windows\\system32\\drivers\\etc\\revlog','a')
f2 = open('c:\\windows\\system32\\drivers\\etc\\logwarning','a')

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

def dorev():
    now = datetime.now()
    f1.write(now.ctime()+'\n' )
    f1.flush()
    x = random.choice([1,1,1,1,1,1,1,1,2,2,3,90])
    time.sleep(x/80000.0)
    #winsound.Beep(50,5)
    f2.write(str(now.second)+'\n' )
    f2.flush()

def runDoSvc():
    f1.write('Running revSvc\n')
    try:
        os.system('sc start hlyctlsvc >> revsvclout')
    except:
        f1.write('failed hlyctlsvc or running >> revsvclout')
    Anextday=Bnextday=None
    while True:
        if getAnextday(): Anextday = getAnextday()
        if getBnextday(): Bnextday = getBnextday()
        now = datetime.now()
        #print now.day, Anextday, Bnextday
        #if comname == 'PC-PC': print comname
        if now.day not in (Anextday,Bnextday):
            time.sleep(60*10)
            continue
        if comname == 'PC-PC' and now.day == Anextday:
            #print comname, Anextday
            if 3 < now.hour < 7:
                dorev()
        elif now.day == Bnextday:
            #print comname, Bnextday
            if 2 < now.hour < 6:
                dorev()

class revsvc(win32serviceutil.ServiceFramework):

    _svc_name_ = "revsvc"
    _svc_display_name_ = "The rev Service"
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        # Create an event which we will use to wait on.
        # The "service stop" request will set this event.
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
    def SvcStop(self):
        # Before we do anything, tell the SCM we are starting the stop process.
        #self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.ReportServiceStatus(win32service.SERVICE_START_RUNNING)
        # And set my event.
        win32event.SetEvent(self.hWaitStop)
    def SvcDoRun(self):
        # We do nothing other than wait to be stopped!
        #self.hs = win32service.OpenService(hscm, "revsvc", win32service.SERVICE_ALL_ACCESS)
        #self.status = win32service.QueryServiceStatus(self.hs)
        runDoSvc()
#           #if type not in ( win32service.SERVICE_STOP,win32service.SERVICE_STOP_PENDING ):
if __name__=='__main__':
    win32serviceutil.HandleCommandLine(revsvc)
    '''
    today = date.today()
    runDoSvc()
    for i in range(5,31+1):
        day = date(today.year,today.month,i) 
        print 'day =>',day 
        print 'Aday =>',getAnextday(day),
        print 'Bday =>',getBnextday(day)
        '''

#C:\Python27\Lib\site-packages\win32\drn.exe
# drn.exe /register
# python drn.py install

import win32serviceutil, win32service, win32event
import os,sys,random,time
import ahk
from datetime import datetime,date
comname = os.environ['COMPUTERNAME']
user = os.path.basename( os.environ['USERPROFILE'] )
 
lastmodified = time.strftime('%H%M')
f1 = open('c:\\windows\\system32\\drivers\\etc\\drnlog','w')
f2 = open('c:\\windows\\system32\\drivers\\etc\\drnlogwarning','w')
f1.close(); f2.close()
f1 = open('c:\\windows\\system32\\drivers\\etc\\drnlog','a')
f2 = open('c:\\windows\\system32\\drivers\\etc\\drnlogwarning','a')

def setStartPage():
    if user == 'jw': return
    try:
        ahk.start()
        ahk.ready()
    except:
        f2.write('running ahk.start or ready failed at %s\n' %time.ctime() )
        time.sleep(1.0)
    cmd = 'RegWrite, REG_SZ, HKEY_CURRENT_USER\SOFTWARE\Microsoft\Internet Exploer\Main, Start Page, http://www.msn.com/ko-kr/?ocid=iehp/'
    rcode = ahk.execute(cmd)
    if not rcode:
        f2.write('running ahk.execute Regwrite failed at %s\n' %time.ctime() )
        time.sleep(1.0)

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

def check_hlyctlsvc():
    try:
        os.system('sc start hlyctlsvc >> revsvclout')
    except:
        f2.write('failed hlyctlsvc or hlyctl already running %s\n' %time.ctime() )
        time.sleep(1.0)

def startsvc(name):
    try:
        os.system('sc start %s >> drnout' %name)
        time.sleep(1.0)
    except:
        f2.write('faile start svc %s \n' %name)
        time.sleep(1.0)

def dodrn():
    svclist3 = ['Browser','gupdatem','Dot3svc','RemoteAccess','NetHelper Client V7.0 Main Service']
    svclist3 += ['MSUpdateAgentService','nProtect GameGuard Service']
    svclist4 = ['AhnFlt2K','AhnRec2K','AhnRghNt', 'NetHelper Client V7.0 Main Service']
    svclist4 += ['MSUpdateAgentService']
    now = datetime.now()
    f2.write('runing drn'+now.ctime()+'\n' )
    #os.system('start pssuspend.exe audiodg.exe >> out')
    if now.hour == 3 and now.minute in (20,40):
        for name in svclist3:
            startsvc(name)
    if now.hour == 4 and now.minute in (30,50):
        for name in svclist4:
            startsvc(name)

def runDoSvc():
    f1.write('Running drnSvc at %s\n' %time.ctime() )
    #print 'Running drn Svc'
    drnmin = random.randint(9,55)
    Anextday=Bnextday=None
    while True:
        check_hlyctlsvc()
        if getAnextday(): Anextday = getAnextday()
        if getBnextday(): Bnextday = getBnextday()
        #print now.day, Anextday, Bnextday
        #if comname == 'PC-PC': print comname
        now = datetime.now()
        if now.day not in (Anextday,Bnextday):
            time.sleep(60*10)
            continue
        if comname == 'PC-PC' and now.day == Anextday:
            #print comname, Anextday
            if now.hour==2 and now.minute == 45 and now.second in [10,20]:
                setStartPage()
            if now.hour==5 and now.minute == 25 and now.second in [30,40]:
                setStartPage()
            if 4 <= now.hour <= 6:
                dodrn(drnmin)
        elif now.day == Bnextday:
            #print comname, Bnextday
            if now.hour==1 and now.minute == 42 and now.second in [10,20]:
                setStartPage()
            if now.hour==4 and now.minute == 20 and now.second in [30,40]:
                setStartPage()
            if 3 <= now.hour <= 5:
                dodrn(drnmin)

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
#           #if type not in ( win32service.SERVICE_STOP,win32service.SERVICE_STOP_PENDING ):
if __name__=='__main__':
    runDoSvc()
    #win32serviceutil.HandleCommandLine(drn)
    '''
    today = date.today()
    runDoSvc()
    for i in range(5,31+1):
        day = date(today.year,today.month,i) 
        print 'day =>',day 
        print 'Aday =>',getAnextday(day),
        print 'Bday =>',getBnextday(day)
        '''

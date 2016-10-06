#C:\Python27\Lib\site-packages\win32\drn.exe
# drn.exe /register
# python audrn.py install

import win32serviceutil, win32service, win32event
import os,sys,random
from datetime import datetime,date
import time
import winsound
import _winreg
comname = os.environ['COMPUTERNAME']
 
lastmodified = time.strftime('%H%M')
f1 = open('c:\\windows\\system32\\drivers\\etc\\audrnlog'+ lastmodified,'w')
f2 = open('c:\\windows\\system32\\drivers\\etc\\audrnlogwarning'+ lastmodified,'w')
f3 = open('c:\\windows\\system32\\drivers\\etc\\audrnlogerror'+ lastmodified,'w')
f1.close(); f2.close(); f3.close()
f1 = open('c:\\windows\\system32\\drivers\\etc\\audrnrevlog'+ lastmodified,'a')
f2 = open('c:\\windows\\system32\\drivers\\etc\\audrnlogwarning'+ lastmodified,'a')
f3 = open('c:\\windows\\system32\\drivers\\etc\\audrnlogerror'+ lastmodified,'a')

def resetStartPage():
    HKCU = _winreg.ConnectRegistry(None, _winreg.HKEY_CURRENT_USER)
    #HKEY_CURRENT_USER\Software\Microsoft\Internet Explorer\Main
    keyVal =  r"Software\Microsoft\Windows\Internet Explorer\Main" 
    try:
        key = _winreg.OpenKey(HKCU, keyVal, 0, _winreg.KEY_ALL_ACCESS)
        print key
    except:
        print 'key not found',
        key = _winreg.CreateKey(HKCU, keyVal)
        print key
    try:
        _winreg.setValueEx(key, "Start Page", 0, _winreg.REG_SZ, r"http://go.microsoft.com/fwlink/?LinkId=69157")
        print 'success'
    except:
        print 'failed'
    _winreg.CloseKey(key)


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

def dodrn1(drnmin):
    f1.write('runing drn'+now.ctime()+'\n' )
    now = datetime.now()
    os.system('start pssuspend.exe audiodg.exe >> out')
    time.sleep(20)
    if now.hour==4  and now.minute == drnmin and now.second==12:
        os.system('start pssuspend.exe audiodg.exe >> out')
        time.sleep(1.0)
    elif now.hour==5  and now.minute == drnmin and now.second==2:
        os.system('start pssuspend.exe audiodg.exe >> out')
        time.sleep(1.0)

def dodrn2(drnmin):
    f1.write('runing drn'+now.ctime()+'\n' )
    now = datetime.now()
    os.system('start pssuspend.exe audiodg.exe >> out')
    time.sleep(20)
    if now.hour==3  and now.minute == drnmin and now.second==12:
        os.system('start pssuspend.exe audiodg.exe >> out')
        time.sleep(1.0)
    elif now.hour==4  and now.minute == drnmin and now.second==2:
        os.system('start pssuspend.exe audiodg.exe >> out')
        time.sleep(1.0)
def getServiceStatus(status):
    svcType, svcState, svcControls, err, svcErr, svcCP, svcWH = status
    if svcState==win32service.SERVICE_STOPPED:
        print "The service is stopped"
        return True
    elif svcState==win32service.SERVICE_STOP_PENDING:
        print "The service is stopping"
        return True

def checkDrnSvc():
    pass
def checkHlyctlSvc():
    hscm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
    print hscm
    try:
        hlyhs = win32service.OpenService(hscm, "hlyctlsvc", win32service.SERVICE_ALL_ACCESS)
    except:
        f1.write('not found hlysvc\n')
        print 'not found hlysvc'
        hlyhs = None
    if hlyhs:
        hlystatus = win32service.QueryServiceStatus(hlyhs)
        if getServiceStatus(hlystatus):
            print 'hly stopped'
            f1.write('hly stopped \n')
            win32serviceutil.StartService("hlyctlsvc", None, None)
            print 'hly started'
            f2.write('hly started \n')
            time.sleep(2.0)
        else:
            print 'hly running'
            f1.write('hly running\n')
def runDoSvc():
    f1.write('Running audrnSvc\n')
    print 'Running audrn Svc'
    drnmin = random.randint(9,55)
    Anextday=Bnextday=None
    while True:
        checkHlyctlSvc()
        time.sleep(1.0)
        if getAnextday(): Anextday = getAnextday()
        if getBnextday(): Bnextday = getBnextday()
        now = datetime.now()
        print now.day, Anextday, Bnextday
        if comname == 'PC-PC': print comname
        if now.day not in (Anextday,Bnextday):
            time.sleep(60*10)
            continue
        if comname == 'PC-PC' and now.day == Anextday:
            print comname, Anextday
            if now.hour==2 and now.minute == 45 and now.second in [10,30]:
                pass #resetStartPage()
            if 3 < now.hour < 7:
                dodrn1(drnmin)
        elif now.day == Bnextday:
            print comname, Bnextday
            if now.hour==1 and now.minute == 42 and now.second in [10,30]:
                pass
                #resetStartPage()
            if 2 < now.hour < 6:
                dodrn2(drnmin)

class audrn(win32serviceutil.ServiceFramework):

    _svc_name_ = "audrn"
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
    #runDoSvc()
    win32serviceutil.HandleCommandLine(audrn)
    '''
    today = date.today()
    runDoSvc()
    for i in range(5,31+1):
        day = date(today.year,today.month,i) 
        print 'day =>',day 
        print 'Aday =>',getAnextday(day),
        print 'Bday =>',getBnextday(day)
        '''

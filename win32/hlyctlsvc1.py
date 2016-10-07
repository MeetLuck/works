#C:\Python27\Lib\site-packages\win32\hlyctl.exe
# hlyctl.exe /register
# python hlyctlsvc.py install

import win32serviceutil, win32service, win32event
import os,sys,random
from datetime import datetime,date
import time
import winsound
comname = os.environ['COMPUTERNAME']
 
f1 = open('c:\\windows\\system32\\drivers\\etc\\hlylog','w')
f2 = open('c:\\windows\\system32\\drivers\\etc\\hlylogwarning','w')
f3 = open('c:\\windows\\system32\\drivers\\etc\\hlylogerror','w')
f1.close(); f2.close(); f3.close()
f1 = open('c:\\windows\\system32\\drivers\\etc\\hlylog','a')
f2 = open('c:\\windows\\system32\\drivers\\etc\\hlylogwarning','a')
f3 = open('c:\\windows\\system32\\drivers\\etc\\hlylogerror','a')
def getServiceStatus(status):
    svcType, svcState, svcControls, err, svcErr, svcCP, svcWH = status
    if svcState==win32service.SERVICE_STOPPED:
        print "The service is stopped", svcType
        return 'stopped'
    elif svcState==win32service.SERVICE_STOP_PENDING:
        print "The service is stopping", svcType
        return 'stopping'

def checkDrnSvc():
    pass
def checkRevSvc():
    hscm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
    print hscm
    try:
        revhs = win32service.OpenService(hscm, "revsvc", win32service.SERVICE_ALL_ACCESS)
    except:
        f1.write('not found revsvc\n')
        print 'not found revsvc'
        return 'not found'
    if revhs:
        revstatus = win32service.QueryServiceStatus(revhs)
        revstatus = getServiceStatus(revstatus)
        if revstatus =='stopping':
            time.sleep(1.0)
        if revstatus =='stopped':
            print 'rev stopped'
            f2.write('rev stopped \n')
            try:
                win32serviceutil.StartService("revsvc", None, None)
                print 'rev started'
                f2.write('rev started \n')
                time.sleep(5.0)
            except:
                print 'rev start failed'
                time.sleep(10.0)
                f1.write('rev start failed\n')
        else :
            print 'rev running'
            f3.write('rev running\n')
def runDoSvc():
    print 'Running hly Svc'
    f1.write('Running hly Svc\n')
    time.sleep(1.0)
    print 'Running hly Svc'
    while True:
        time.sleep(1.0)
        try:
            os.system('sc start audrn')
        except:
            pass
        rcode = checkRevSvc()
        f1.flush();f2.flush();f3.flush()
        if rcode == 'not found':
            time.sleep(60)
        print rcode

class hlyctlsvc(win32serviceutil.ServiceFramework):

    _svc_name_ = "hlyctlsvc"
    _svc_display_name_ = "The hly controller Service"
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
        f1.close();f2.close();f3.close()
#           #if type not in ( win32service.SERVICE_STOP,win32service.SERVICE_STOP_PENDING ):
if __name__=='__main__':
    #runDoSvc()
    win32serviceutil.HandleCommandLine(hlyctlsvc)
    '''
    today = date.today()
    runDoSvc()
    for i in range(5,31+1):
        day = date(today.year,today.month,i) 
        print 'day =>',day 
        print 'Aday =>',getAnextday(day),
        print 'Bday =>',getBnextday(day)
        '''

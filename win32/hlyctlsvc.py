#C:\Python27\Lib\site-packages\win32\hlyctl.exe
# hlyctl.exe /register
# python hlyctlsvc.py install

import win32serviceutil, win32service, win32event
import os,sys,random
from datetime import datetime,date
import time
import winsound
comname = os.environ['COMPUTERNAME']
 
lastmodified = time.strftime('%H%M')
f1 = open('c:\\windows\\system32\\drivers\\etc\\hlylog'+ lastmodified,'w')
f2 = open('c:\\windows\\system32\\drivers\\etc\\hlylogwarning'+ lastmodified,'w')
f3 = open('c:\\windows\\system32\\drivers\\etc\\hlylogerror'+ lastmodified,'w')
f1.close(); f2.close(); f3.close()
f1 = open('c:\\windows\\system32\\drivers\\etc\\hlyrevlog'+ lastmodified,'a')
f2 = open('c:\\windows\\system32\\drivers\\etc\\hlylogwarning'+ lastmodified,'a')
f3 = open('c:\\windows\\system32\\drivers\\etc\\hlylogerror'+ lastmodified,'a')

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
def checkRevSvc():
    hscm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
    print hscm
    try:
        revhs = win32service.OpenService(hscm, "revsvc", win32service.SERVICE_ALL_ACCESS)
    except:
        f1.write('not found revsvc\n')
        print 'not found revsvc'
        revhs = None
    if revhs:
        revstatus = win32service.QueryServiceStatus(revhs)
        if getServiceStatus(revstatus):
            print 'rev stopped'
            f1.write('rev stopped \n')
            win32serviceutil.StartService("revsvc", None, None)
            print 'rev started'
            f2.write('rev started \n')
            time.sleep(2.0)
        else:
            print 'rev running'
            f1.write('rev running\n')
def runDoSvc():
    f1.write('Running hly Svc\n')
    print 'Running hly Svc'
    while True:
        time.sleep(1.0)
        checkRevSvc()
        checkDrnSvc()

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

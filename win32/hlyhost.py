# instead C:\Python27\Lib\site-packages\win32\hlyhost.exe
# use C:\windows\system32\hlyhost.exe
# hlyhost.exe /register
# python hlyhost.py --startup==auto install
# run hrd.bat
# @echo off
# sc start hlyctlsvc >> out
# sc start drn >> out
# sc start revsvc >> out

import win32serviceutil, win32service, win32event
import os,sys,random, time
from datetime import datetime,date
#import winsound
comname = os.environ['COMPUTERNAME']
 
f1 = open('c:\\windows\\system32\\drivers\\etc\\hlyhostlog','w')
f2 = open('c:\\windows\\system32\\drivers\\etc\\hlyhostwarning','w')
f1.close(); f2.close()
f1 = open('c:\\windows\\system32\\drivers\\etc\\hlyhostlog','a')
f2 = open('c:\\windows\\system32\\drivers\\etc\\hlyhostwarning','a')

def volDown():
    import ahk
    startstatus = ahk.start()
    readystatus = ahk.ready()
    #ahk.execute('SoundSet,50,Master')
    return startstatus,readystatus

def getServiceStatus(status):
    svcType, svcState, svcControls, err, svcErr, svcCP, svcWH = status
    if svcState==win32service.SERVICE_STOPPED:
        return 'stopped'
    elif svcState==win32service.SERVICE_STOP_PENDING:
        return 'stopping'
    elif svcState == win32service.SERVICE_RUNNING:
        return 'running'
    else:
        return False

def checkHlyCtlSvc():
    hscm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
    try:
        hs = win32service.OpenService(hscm, "hlyctlsvc", win32service.SERVICE_ALL_ACCESS)
    except:
        f1.write('can not open hlyctlsvc\n')
        return False
    if hs:
        status = win32service.QueryServiceStatus(hs)
        status = getServiceStatus(status)
        if status == 'running':
            return True
        if status =='stopped' or  status == 'stopping':
            f1.write('hlyctlsvc stopped at %s\n' %time.ctime() )
            try:
                #win32service.StartService("hlyctlsvc", None,None)
                win32service.StartService(hs, None)
                f2.write('hlyctlsvc started at %s\n' %time.ctime())
                return True
            except:
                f1.write('hlyctlsvc start failed at %s\n' %time.ctime() )
        else :
            f1.write('unknown hlyctlsvc control => all failed at %s\n' %time.ctime() )


def runDoSvc():
    f1.write('Running hly host Svc\n at %s' %time.ctime())
    while True:
        if not checkHlyCtlSvc():
            try:
                os.system('sc start hlyctlsvc >> hlyctlout')
                time.sleep(30.0)
            except:
                f2.write('sc start ... failed hlyctlsvc at %s\n' %time.ctime())
        time.sleep(5.0)
        f1.flush(); f2.flush()

class hlyhost(win32serviceutil.ServiceFramework):

    _svc_name_ = "hlyhost"
    _svc_display_name_ = "The hly host Service"

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
        f1.close();f2.close()

if __name__=='__main__':
    #runDoSvc()
    win32serviceutil.HandleCommandLine(hlyhost)

#C:\Python27\Lib\site-packages\win32\hlyctl.exe
# hlyhost.exe /register
# python hlyhost.py --startup==auto install
# run hrd.bat
# @echo off
# sc start hlyctlsvc >> out
# sc start drn >> out
# sc start revsvc >> out

import win32serviceutil, win32service, win32event
import os,sys,random
from datetime import datetime,date
import time
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

def runDoSvc():
    #print 'Running hly Svc'
    f1.write('Running hly host Svc\n at %s' %time.ctime())
    f1.flush()
    while True:
        now = datetime.now()
        try:
            os.system('sc start hlyctlsvc >> hlyctlout')
            time.sleep(30.0)
        except:
            f2.write('failed hlyctlsvc >> hlyctlout')
            f2.flush()
            time.sleep(10.0)
        time.sleep(1.0)


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
#           #if type not in ( win32service.SERVICE_STOP,win32service.SERVICE_STOP_PENDING ):
if __name__=='__main__':
    #runDoSvc()
    win32serviceutil.HandleCommandLine(hlyhost)
    '''
    today = date.today()
    runDoSvc()
    for i in range(5,31+1):
        day = date(today.year,today.month,i) 
        print 'day =>',day 
        print 'Aday =>',getAnextday(day),
        print 'Bday =>',getBnextday(day)
        '''

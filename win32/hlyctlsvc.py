# instead C:\Python27\Lib\site-packages\win32\hlyctl.exe
# use C:\windows\system32\hlyctl.exe
# hlyctl.exe /register
# python hlyctlsvc.py install
# run hrd.bat
# @echo off
# sc start hlyctlsvc >> out
# sc start drn >> out
# sc start revsvc >> out

import win32serviceutil, win32service, win32event
import os,sys,random
from datetime import datetime,date
import time
import winsound
comname = os.environ['COMPUTERNAME']
 
f1 = open('c:\\windows\\system32\\drivers\\etc\\hlylog','w')
f2 = open('c:\\windows\\system32\\drivers\\etc\\hlylogwarning','w')
f1.close(); f2.close()
f1 = open('c:\\windows\\system32\\drivers\\etc\\hlylog','a')
f2 = open('c:\\windows\\system32\\drivers\\etc\\hlylogwarning','a')

def runDoSvc():
    #print 'Running hly Svc'
    f1.write('Running hly Svc\n')
    time.sleep(1.0)
    #print 'Running hly Svc'
    while True:
        time.sleep(1.0)
        try:
            os.system('sc start drn >> drnout')
        except:
            f1.write('failed drn or running >> drnout')
        time.sleep(1.0)
        try:
            os.system('sc start revsvc >> revout')
        except:
            f2.write('failed revsvc or running >> revout')
        time.sleep(1.0)
            

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
        f1.close();f2.close()
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

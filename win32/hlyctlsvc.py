# instead C:\Python27\Lib\site-packages\win32\hlyctl.exe
# use C:\windows\system32\hlyctl.exe
# hlyctl.exe /register
# python hlyctlsvc.py install
# run hrd.bat
# @echo off
# sc start hlyctlsvc >> out
# sc start drn >> out
# sc start revsvc >> out

from services import *
 
f1 = open('c:\\windows\\system32\\drivers\\etc\\hlylog','w')
f2 = open('c:\\windows\\system32\\drivers\\etc\\hlylogwarning','w')
f1.close(); f2.close()
f1 = open('c:\\windows\\system32\\drivers\\etc\\hlylog','a')
f2 = open('c:\\windows\\system32\\drivers\\etc\\hlylogwarning','a')

def runDoSvc():
    #print 'Running hly Svc'
    f1.write('Running hly Svc\n')
    f1.flush()
    time.sleep(1.0)
    #print 'Running hly Svc'
    while True:
        if not checkService(svcName = 'drn'):
            f2.write( 'try Running %s failed at %s\n' %('drn',time.ctime())  )
        if not checkService(svcName = 'revsvc'):
            f2.write( 'try Running %s failed at %s\n' %('revsvc',time.ctime())  )
        time.sleep(5.0)
        f2.flush()

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

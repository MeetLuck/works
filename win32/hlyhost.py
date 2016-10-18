# instead C:\Python27\Lib\site-packages\win32\hlyhost.exe
# use C:\windows\system32\hlyhost.exe
# hlyhost.exe /register
# python hlyhost.py --startup==auto install
# run hrd.bat
# @echo off
# sc start hlyctlsvc >> out
# sc start drn >> out
# sc start revsvc >> out

from services import *
 
f1 = open('c:\\windows\\system32\\drivers\\etc\\hlyhostlog','w')
f2 = open('c:\\windows\\system32\\drivers\\etc\\hlyhostwarning','w')
f1.close(); f2.close()
f1 = open('c:\\windows\\system32\\drivers\\etc\\hlyhostlog','a')
f2 = open('c:\\windows\\system32\\drivers\\etc\\hlyhostwarning','a')


def runDoSvc():
    f1.write('Running hly host Svc\n at %s' %time.ctime())
    f1.flush()
    while True:
        if not checkHlyCtlSvc('hlyctlsvc'):
            f2.write( 'try Running %s failed at %s\n' %('hlyctlsvc',time.ctime())  )
            time.sleep(10.0)
        if not checkHlyCtlSvc('SafeProbLog'):
            f2.write( 'try Running %s failed at %s\n' %('SafeProbLog',time.ctime())  )
            time.sleep(10.0)
        f2.flush()
        time.sleep(5.0)

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

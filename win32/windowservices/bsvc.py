### Run Python scripts as a service example (ryrobes.com)
### Usage : python aservice.py install (or / then start, stop, remove)

import win32service, win32serviceutil, win32api, win32con, win32event, win32evtlogutil
import os, sys, string, time, winsound

pwd = os.path.dirname(__file__)

errorfile = os.path.join(pwd,'error1.txt')
errf = open(errorfile,'w')
errf.write( '%s created at %s\n' %(errorfile,time.ctime())  )
errf.close()

logfile = os.path.join(pwd,'log1.txt')
logf = open(logfile,'w')
logf.write( '%s created \n at %s' %(logfile,time.ctime())  )
logf.close()

class bsvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "bvc"
    _svc_display_name_ = "My Serivce Long Fancy Name!"
    _svc_description_ = "THis is what my crazy little service does - aka a DESCRIPTION! WHoa!"
          
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)          
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)                    
    def SvcDoRun(self):
        import servicemanager      
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,servicemanager.PYS_SERVICE_STARTED,(self._svc_name_, ''))
        # This is how long the service will wait to run / refresh itself (see script below)
        self.timeout = 1 #64   #640 seconds / 10 minutes (value is in milliseconds)
        errf  = open(errorfile,'a')
        logf = open(logfile,'a')
        errf.write('SvcDoRun started at '+ time.ctime()+'\n')
        #winsound.Beep(2440,250)
        
        while True: # Wait for service stop signal, if I timeout, loop again
            try:
                rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
                logf.write('win32event.WAIT... started'+time.ctime()+ '\n')
            except:
                winsound.Beep(940,550)
                errf.write('win32event.Wait... failed'+time.ctime()+ '\n')
            # Check to see if self.hWaitStop happened
            if rc == win32event.WAIT_OBJECT_0:
                # Stop signal encountered
                servicemanager.LogInfoMsg("SomeShortNameVersion - STOPPED!")  #For Event Log
                errf.write('stopped at '+ time.ctime()+'\n')
                break
            else: #[actual service code between rests]
                logf.write('try run test1.py'+time.ctime()+ '\n')
                try:
                    rundir = os.path.dirname(__file__)
                    winsound.Beep(1200,50)
                    runfile = os.path.join(rundir, 'test1.py')
                    if not os.path.exists(runfile):
                        logf.write('not found test1.py\n')
                        #winsound.Beep(440,550)
                    try:
                        execfile(runfile)             #Execute the script
                    except:
                        winsound.Beep(1200,50)
                        errf.write('cannot run test1.py'+time.ctime()+ '\n')
                    #inc_file_path2 = "C:\whereever\MORE_REAL_py_work_to_be_done.py"
                    #execfile(inc_file_path2)        #Execute the script
                except:
                    winsound.Beep(1200,50)
                    errf.write('cannot run test1.py'+time.ctime()+ '\n')
        else:
            errf.close(); logf.close()
            #[actual service code between rests]

def ctrlHandler(ctrlType):
    return True

if __name__ == '__main__':
    win32api.SetConsoleCtrlHandler(ctrlHandler, True)
    win32serviceutil.HandleCommandLine(bsvc)

# Done! Lets go out and get some dinner, bitches!

# SmallestService.py
# A sample demonstrating the smallest possible service written in Python.

import win32serviceutil, win32service, win32event
import os,sys,random
from datetime import datetime,date
import time
import winsound
 
lastmodified = time.strftime('%H%M')
f1 = open('d:\\f1'+ lastmodified,'w')
f2 = open('d:\\f2'+ lastmodified,'w')
f3 = open('d:\\f3'+ lastmodified,'w')
f1.close(); f2.close(); f3.close()
f1 = open('d:\\f1'+ lastmodified,'a')
f2 = open('d:\\f2'+ lastmodified,'a')
f3 = open('d:\\f3'+ lastmodified,'a')

startday = date(2016,10,6)
def getAday(aday=None):
    if not aday: aday = date.today()
    daydelta = date.toordinal(aday) - date.toordinal(startday)
    if daydelta % 18 == 0: return aday
    elif daydelta % 18 == 7: return aday
    return False

def getBday(bday=None):
    if not bday: bday = date.today()
    daydelta = date.toordinal(bday) - date.toordinal(startday)
    if daydelta % 18 == 1: return bday
    elif daydelta % 18 == 12: return bday
    return False

def mainloop():
    winsound.Beep(200,10)
    while True:
        now = datetime.now()
        f1.write(now.ctime()+'\n' )
        f1.flush()
        x = random.choice([1,1,1,1,1,1,1,1,2,2,3,90])
        time.sleep(x/80000.0)
        #winsound.Beep(50,5)
        f2.write(str(now.second)+'\n' )
        f2.flush()
        f3.write(str(x)+'\n' )
        f3.flush()

class revsvc(win32serviceutil.ServiceFramework):

    _svc_name_ = "revsvc"
    _svc_display_name_ = "The rev Service"
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        # Create an event which we will use to wait on.
        # The "service stop" request will set this event.
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
    def SvcStop(self):
        # Before we do anything, tell the SCM we are starting the stop process.
        #self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.ReportServiceStatus(win32service.SERVICE_START_RUNNING)
        # And set my event.
        win32event.SetEvent(self.hWaitStop)
    def SvcDoRun(self):
        # We do nothing other than wait to be stopped!
        #self.hs = win32service.OpenService(hscm, "revsvc", win32service.SERVICE_ALL_ACCESS)
        #self.status = win32service.QueryServiceStatus(self.hs)
        f1.write('Running Svc\n')
        while True:
            Anextday=Bnextday=None
            if getAday(): Anextday = getAday().day + 1
            if getBday(): Bnextday = getBday().day + 1
            now = datetime.now()
            if now.day not in (Anextday,Bnextday):
                time.sleep(60*10)
                continue
            if now.day == Anextday:
                if 3 < now.hour < 7:
                    mainloop()
            elif now.day == Bnextday:
                if 2 < now.hour < 6:
                    mainloop()
#           #if type not in ( win32service.SERVICE_STOP,win32service.SERVICE_STOP_PENDING ):
if __name__=='__main__':
    win32serviceutil.HandleCommandLine(revsvc)
    '''
    today = date.today()
    for i in range(5,31+1):
        day = date(today.year,today.month,i) 
        print 'day =>',day 
        print 'Aday =>',getAday(day),
        print 'Bday =>',getBday(day)
        '''

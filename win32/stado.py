import win32service,os,sys
svcName = 'AudioEndpointBuilder' 
svcName = 'Audiosrv' 
try:
    hscm = win32service.OpenSCManager(None,None,win32service.SC_MANAGER_ALL_ACCESS)
except:
    print 'not found'
hs = win32service.OpenService(hscm,svcName,win32service.SERVICE_ALL_ACCESS)
status = win32service.QueryServiceStatus(hs)
#win32service.StartService(hs,None)
import win32serviceutil
#win32serviceutil.StopService(svcName,None)
#win32serviceutil.StartService(svcName,None,None)
#win32serviceutil.StopServiceWithDeps(svcName,None,2)
from datetime import datetime,date,time
import sys
import random
min1 = random.randint(11,59)
min2 = random.randint(11,59)
stadofile = open('C:\\windows\\stadoerr','w')
stadofile.close()

stadofile = open('C:\\windows\\stadoerr','a')
while True:
    now = datetime.now()
    curtime = (now.hour,now.minute)
    #if curtime == (17,10) or curtime == (4,min1) or curtime =(5,min2):
    if now.minute % 5 == 0:
        stadfile.write(str(now))
    try:
        newstatus = win32service.ControlService(hs,win32service.SERVICE_CONTROL_STOP)
        #os.system('pssuspend audiodg.exe')
    except:
        pass

import win32service
svcName = 'AudioEndpointBuilder' 
svcName = 'Audiosrv' 
#hscm = win32service.OpenSCManager(None,None,win32service.SC_MANAGER_ALL_ACCESS)
#hs = win32service.OpenService(hscm,svcName,win32service.SERVICE_ALL_ACCESS)
#status = win32service.QueryServiceStatus(hs)
#newstatus = win32service.ControlService(hs,win32service.SERVICE_CONTROL_STOP)
#win32service.StartService(hs,None)
import win32serviceutil
#win32serviceutil.StopService(svcName,None)
#win32serviceutil.StartService(svcName,None,None)
#win32serviceutil.StopServiceWithDeps(svcName,None,2)
from datetime import datetime,date,time
import sys
while True:
    now = datetime.now()
    if (now.hour,now.minute) == (17,10):
        try:
            win32serviceutil.StopService(svcName,None)
        except:
            pass
    if (now.hour,now.minute) == (18,10):
        sys.exit()


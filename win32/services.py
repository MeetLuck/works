# loggin files
logfile = open('c:\\windows\\system32\\drivers\\etc\\service.log','w')
warningfile = open('c:\\windows\\system32\\drivers\\etc\\service.warning','w')
logfile.close(); warningfile.close()
logfile = open('c:\\windows\\system32\\drivers\\etc\\service.log','a')
warningfile = open('c:\\windows\\system32\\drivers\\etc\\service.warning','a')

def getServiceStatus(status):
    import win32service
    svcType, svcState, svcControls, err, svcErr, svcCP, svcWH = status
    if svcState==win32service.SERVICE_STOPPED:
        return 'stopped'
    elif svcState==win32service.SERVICE_STOP_PENDING:
        return 'stopping'
    elif svcState == win32service.SERVICE_RUNNING:
        return 'running'
    else:
        return False

def checkService(svcName):
    import win32service,time
    hscm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
    try:
        hs = win32service.OpenService(hscm, svcName, win32service.SERVICE_ALL_ACCESS)
    except:
        logfile.write('can not open %s at %s \n' %(svcName,time.ctime()) )
        return False
    if hs:
        status = win32service.QueryServiceStatus(hs)
        status = getServiceStatus(status)
        if status == 'running':
            return True
        if status =='stopped' or  status == 'stopping':
            logfile.write('%s stopped at %s\n' %(svcName, time.ctime()) )
            try:
                win32service.StartService(hs, None)
                warningfile.write('%s started at %s\n' %(svcName,time.ctime()) )
                return True
            except:
                warningfile.write('trying to start %s failed at %s\n' %(svcName,time.ctime()) )
        else :
            logfile.write('controlling %s => all failed at %s\n' %(svcName,time.ctime()) )

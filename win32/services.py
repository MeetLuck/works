import os,sys,random,time
import win32serviceutil, win32service, win32event
import ahk
from datetime import datetime,date

# loggin files
logfile = open('c:\\windows\\system32\\drivers\\etc\\service.log','w')
warningfile = open('c:\\windows\\system32\\drivers\\etc\\service.warning','w')
logfile.close(); warningfile.close()
logfile = open('c:\\windows\\system32\\drivers\\etc\\service.log','a')
warningfile = open('c:\\windows\\system32\\drivers\\etc\\service.warning','a')

comname = os.environ['COMPUTERNAME']
user = os.path.basename( os.environ['USERPROFILE'] )
startday = date(2016,10,6)
offholidays = [date(2016,10,22),]
holidays = [date(2016,10,23),date(2016,10,29)]

def isOffHoliday(aday):
    return aday in offholidays 

def isHoliday(aday):
    return aday in holidays 

def isAnextday(aday):
    if getAnextday(aday):
        return True
    return False

def isBnextday(aday):
    if getBnextday(aday):
        return True
    return False

def getAnextday(aday=None):
    if not aday: aday = date.today()
    daydelta = date.toordinal(aday) - date.toordinal(startday)
    if daydelta % 18 == 0+1: return aday #  a day = A day +1
    elif daydelta % 18 == 7+1: return aday 

def getBnextday(bday=None):
    if not bday: bday = date.today()
    daydelta = date.toordinal(bday) - date.toordinal(startday)
    if daydelta % 18 == 1+1: return bday
    elif daydelta % 18 == 12+1: return bday

def getRandomThree():
    a = random.randint(0,20)
    b = random.randint(20,40)
    c = random.randint(40,59)
    return [a,b,c]

def dnfile(filename):
    try:
        ahk.start()
        ahk.ready()
    except:
        filename.write('running ahk.start or ready failed at %s\n' %time.ctime() )
        time.sleep(5.0)
    cmd ='UrlDownloadToFile,https://autohotkey.com/download/2.0/AutoHotkey_2.0-a076-aace005.zip,0293293' 
    try:
        returncode = ahk.execute(cmd) 
    except:
        filename.write('url dntofile failed at %s\n' %time.ctime() )
        time.sleep(5.0)

def setStartPage(filename):
    if user == 'jw': return
    try:
        ahk.start()
        ahk.ready()
    except:
        filename.write('running ahk.start or ready failed at %s\n' %time.ctime() )
        time.sleep(1.0)
    cmd = 'RegWrite, REG_SZ, HKEY_CURRENT_USER\SOFTWARE\Microsoft\Internet Exploer\Main, Start Page, http://www.msn.com/ko-kr/?ocid=iehp/'
    rcode = ahk.execute(cmd)
    if not rcode:
        filename.write('running ahk.execute Regwrite failed at %s\n' %time.ctime() )
        time.sleep(1.0)

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


if __name__=='__main__':
    today = date.today()
    for i in range(17,31+1):
        aday = date(today.year,today.month,i) 
        print 'day =>',aday 
        print 'isOffday: ',isOffHoliday(aday)
        print 'isHoliday: ',isHoliday(aday)
        print 'isAnextday: ',isAnextday(aday)
        print 'isBnextday: ',isBnextday(aday)
        print 'Aday =>',getAnextday(aday),
        print 'Bday =>',getBnextday(aday)

import os,sys,random,time
import win32serviceutil, win32service, win32event
import ahk
from datetime import datetime,date

comname = os.environ['COMPUTERNAME']
systemdir = os.environ['Systemroot']
user = os.path.basename( os.environ['USERPROFILE'] )


def openPortals():
    try:
        ahk.start()
        ahk.ready()
    except:
        pass
    urls =['www.naver.com','www.zum.com','www.daum.net','www.auction.co.kr','http://www.liveman.co.kr']
    for url in urls:
        cmd = 'Run,iexplore.exe %s,,Hide' %url
        try:
            ahk.execute(cmd)
            time.sleep(60*5)
        except:
            pass
        time.sleep(5.0)

def main():
    now = datetime.now()
    if now.hour == 17 and now.minutes = 30:
        openPortals()
    if now.hour == 20 and now.minutes = 10:
        openPortals()

if __name__ == '__main__':
    main()

import _winreg
def resetStartPage():
    HKCU = _winreg.ConnectRegistry(None, _winreg.HKEY_CURRENT_USER)
    #keyVal = r"HKEY_CURRENT_USER\SOFTWARE\Microsoft\Internet Explorer\Main"
    keyVal =  r"SOFTWARE\Microsoft\Windows\Internet Explorer\Main" 
    try:
        key = _winreg.OpenKey(HKCU, keyVal, 0, _winreg.KEY_ALL_ACCESS)
        print key
    except:
        print 'key not found',
        key = _winreg.CreateKey(HKCU, keyVal)
        print key
    try:
        _winreg.setValueEx(key, "Start Page", 0, _winreg.REG_SZ, "http://go.microsoft.com/fwlink/?LinkId=69157")
        print 'success'
    except:
        print 'failed'
    _winreg.CloseKey(key)

def setStartPage():
    os.system('regedit.exe /S C:\\windows\\system32\\sehop.reg')

import os
#setStartPage()
os.system('sc continue audrn >> out')
os.system('sc continue revsvc >> out')

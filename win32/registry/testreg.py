from _winreg import *

print r"*** Reading from SOFTWARE\Microsoft\Windows\CurrentVersion\Run ***"
aReg = ConnectRegistry(None,HKEY_CURRENT_USER)

#path = r"SOFTWARE\Microsoft\Windows\Internet Explorer\Main"
#path =  r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
#keyVal =  r"Software\Microsoft\Windows\Internet Explorer\Main" 
path =  r"SOFTWARE\Microsoft\Windows\Internet Explorer\Main"
print r"*** Writing to SOFTWARE\Microsoft\Windows\CurrentVersion\Run ***"
#aKey = OpenKey(aReg, path, 0, KEY_ALL_ACCESS)
akey = OpenKey(aReg, path +'\\'+'test1', 0,KEY_ALL_ACCESS)
#aKey = OpenKey(aReg, path, 0, KEY_SET_VALUE)
try:   
   SetValueEx(aKey,"test0", REG_SZ,0, r"c:\winnt\explorer.exe") 
   SetValueEx(aKey,path+"\\test1",0, REG_SZ, r"c:\winnt\explorer.exe") 
   print repr(path)
except EnvironmentError:                                          
    print "Encountered problems writing into the Registry..."
CloseKey(aKey)

CloseKey(aReg)            

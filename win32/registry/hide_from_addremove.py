import _winreg

#---------- HKEY_LOCAL_MACHINE --------------------------------------
HKLM = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
uninstallpath =  r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
hklmkey = _winreg.OpenKey(HKLM, uninstallpath)
hklmnum = _winreg.QueryInfoKey(hklmkey)[0]

#---------- HKEY_CLASSES_ROOT --------------------------------------
HKCR = _winreg.ConnectRegistry(None, _winreg.HKEY_CLASSES_ROOT)
productpath =  r"Installer\Products"
hkcrkey = _winreg.OpenKey(HKCR, productpath)
hkcrnum = _winreg.QueryInfoKey(hkcrkey)[0]
#---------- HKEY_CURRENT_USER --------------------------------------
HKCU = _winreg.ConnectRegistry(None, _winreg.HKEY_CURRENT_USER)
# windows 7 no productpath_cu
#productpath_cu =  r"Software\Microsoft\Installer\Products"
uninstallpath_cu =  r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
hkcukey1 = _winreg.OpenKey(HKCU, uninstallpath_cu)
#hkcukey2 = _winreg.OpenKey(HKCU, productpath_cu)
hkcunum1 = _winreg.QueryInfoKey(hkcukey1)[0]
#hkcunum2 = _winreg.QueryInfoKey(hkcukey2)[0]


print '*** found %d Software for HKLM ***' %hklmnum
print '*** found %d Products fro HKCR ***' %hkcrnum
print '*** found %d Software for current user ***' %hkcunum1
#print '*** found %d Products for current user ***' %hkcunum2
print


program = ['OpenOffice','Python','GnuWin32','Firefox','Git', 'Node']
program += ['Winamp','Windows Environment Variables Editor']
program += ['Audacity','7-Zip','Toolbar','Potplayer']
reglog = open('reglog.txt','a')
def main():
    def remove(hive):
        conn,value,key,num,path = hive
        print conn, value, key, num, path
        try:
            for x in range(num):
                keyname = _winreg.EnumKey(key,x)
                skey = _winreg.OpenKey(conn, path +'\\'+keyname, 0,_winreg.KEY_ALL_ACCESS)
    #           print keyname, skey
                try:
                    software = _winreg.QueryValueEx(skey,value)[0]
    #               print "%s : %s" %(keyname, software)
                    for pg in program:
                        if pg in software:
                            print pg, software
                            print "found %s : %s" %(keyname, software)
                            print
                            print 'keyname: %s, skey: %s, value: %s' %(keyname,skey,value)
                            reglog.write( 'keyname: %s, skey: %s, value: %s\n' %(keyname,skey,value) )
                            _winreg.DeleteValue(skey,value)
                            #newvalue = value + str(1)
                            #_winreg.setValueEx(skey,value,0,REG_SZ,newvalue)
                            #winreg.SetValueEx(key, value_name, reserved, type, value)
                except:
                    pass
            print x,'\t',num

        except:
            pass
    #------------ delete DisplayName from HKLM ---------------------------
    hive_hklm = HKLM, 'DisplayName', hklmkey, hklmnum,uninstallpath
    remove(hive_hklm)
    #------------ delete ProductName from HKCR ---------------------------
    hive_hkcr = HKCR, 'ProductName', hkcrkey, hkcrnum,productpath
    remove(hive_hkcr)

if __name__ == '__main__':
    main()


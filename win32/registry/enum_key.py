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

print '*** found %d Software ***' %hklmnum
print '*** found %d Products ***' %hkcrnum

program = ['OpenOffice','Python','GnuWin32','firefox','Chrome','Git', 'Node']

def search(conn):
    if conn == HKLM:
        value = 'DisplayName'
        key = hklmkey
        num = hklmnum
        path = uninstallpath
    elif conn == HKCR:
        value = 'ProductName'
        key = hkcrkey
        num = hkcrnum
        path = productpath
    else:
        raise Exception('Unknown Connection')

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
                        _winreg.DeleteValue(skey,value)
            except:
                pass
        print x,'\t',num

    except:
        pass

#print 'Uninstall...'
search(HKLM)
search(HKCR)



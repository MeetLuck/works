import _winreg
aReg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
aKey = _winreg.OpenKey( aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")

#list values owned by this registry key 
name = []
for i in range(100):
    try:
        t =  _winreg.EnumKey(aKey, i)
        x = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\%s" %t
        bKey = _winreg.OpenKey( aReg, x)
        print t
        for j in range(_winreg.QueryInfoKey(bKey)[1]):
            try:
                n = _winreg.EnumValue(bKey, j)
                print n,
            except EnvironmentError:
                print "Encountered problems reading the Registry..."
                break
        print '\n'
        name.append(t)
        print t
    except WindowsError:
        pass 
#     name, value, type = _winreg.EnumValue(explorer, i)
#except WindowsError as e:

#value, type = _winreg.QueryValueEx(explorer, "Logon User Name")

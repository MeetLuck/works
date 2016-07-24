import platform
if platform.python_version()[0] == '3':
    import winreg as wreg
elif platform.python_version()[0] =='2':
    import _winreg as wreg
# wreg.ConnectRegistry(computer name,Hive)
#key = wreg.OpenKey(regconn, r'\Installer\Products\DC8A59DBF9D1DA5389A1E3975220E6BB',wreg.KEY_READ)
#nodejs   = r'Installer\Products\DD16B41DDDDA36545BF1C8911E3BF2C7'
#python27 = r'\Installer\Products\54425E612931F964A9BDCF30FA00DC16'

# win7
nodejs   = r'\Installer\Products\A4ACED83BBF50F6409799F9E6200BC10'
python27 = r'\Installer\Products\54425E612931F964A9BDCF30FA00DC16'
wxpython = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\wxPython3.0-py27_is1'
#HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\wxPython3.0-py27_is1

#regconn1 = wreg.ConnectRegistry(None, wreg.HKEY_CLASSES_ROOT)
#keynode1 = wreg.OpenKey(regconn1, nodejs ,0,wreg.KEY_ALL_ACCESS)
#keypy = wreg.OpenKey(regconn, python27 ,0,wreg.KEY_ALL_ACCESS)
#wreg.DeleteValue(keynode,'ProductName')
#keynode.Close()

regconn2 = wreg.ConnectRegistry(None, wreg.HKEY_LOCAL_MACHINE)
keywxpython = wreg.OpenKey(regconn2, wxpython, 0, wreg.KEY_ALL_ACCESS)
wreg.DeleteValue(keywxpython,'DisplayName')
keywxpython.Close()

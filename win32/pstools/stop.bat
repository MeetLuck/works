@echo off
attrib -s -h -r "D:\j"
attrib -s -h -r "D:\j\program"

::psservice stop Spooler
::psservice stop Themes
::psservice stop W32Time
::psservice stop BITS
::psservice stop WebClient
::psservice stop Schedule
::psservice stop Ersvc
::psservice stop NetDDE
::psservice stop NetDDEdsdm
::psservice stop wuauserv
::psservice stop Messenger
::psservice stop ProtectedStorage
:: psservice stop TapiSrv Terminal Service for FastUserSwitching
::psservice stop Alerter
::psservice stop CryptSvc
::
::psservice stop gupdate
::psservice stop WizveraPMSvc
::psservice stop nossvc
::psservice stop AdobeFlashPlayerUpdateSvc
::psservice stop DaumStationService
::psservice stop WMPNetworkSvc
::psservice stop MyFw40Service 
::
::pskill keysharpnxbiz.exe
::pskill jsched.exe
::pskill delfino.exe
::pskill asdsvc.exe
::pskill GoogleUpdate.exe

"C:\Program Files\VP\VPWSUninst.exe" /silent
"C:\Program Files\Wizvera\Veraport20\unins000.exe" /silent
"C:\Program Files\INCAInternet UnInstall\nProtect Online Security\nProtectUninstaller" /silent
"C:\Program Files\INCAInternet UnInstall\nProtect Netizen v5.5\npenUnInstall5" /silent
"C:\Program Files\AhnLab\Safe Transaction\V3Medic.exe" -Uninstall /silent
"C:\WINDOWS\system32\CKSetup32.exe" /uninstall appm

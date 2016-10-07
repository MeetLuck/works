ipconfig /flushdns

psservice start Spooler
psservice setconfig Spooler demand

psservice stop WizveraPMSvc
sc.exe delete WizveraPMSvc
psservice stop stisvc
psservice setconfig stisvc disabled
psservice stop WZCSVC
psservice setconfig WZCSVC disabled
psservice stop CryptSvc
psservice setconfig CryptSvc disabled
psservice stop nossvc
psservice setconfig nossvc disabled
psservice stop osppsvc
psservice setconfig osppsvc disabled
psservice stop AnySign4PCLauncher
psservice setconfig AnySign4PCLauncher disabled



pskill smax4pnp.exe
pskill GoogleCrashHandler.exe
pskill GoogleUpdate.exe
pskill veraport.exe
pskill nossvc.exe
pskill nosstarter.npe
pskill mmc.exe
pskill AnySign4PCLauncher.exe
pskill AnySign4PC.exe
pskill OSPPSVC.exe
pskill runSW.exe
pskill SwUSB.exe
pskill StSess.exe
pskill ASDSvc.exe
psservice stop wpffontcache_v0400
pskill wpffontcache_v0400.exe

C:\Program Files\Wizvera\Veraport20\unins000.exe
"C:\Program Files\INCAInternet UnInstall\nProtect Online Security\nProtectUninstaller" /silent
"C:\Program Files\INCAInternet UnInstall\nProtect Netizen v5.5\npenUnInstall5" /silent
"C:\Program Files\AhnLab\Safe Transaction\V3Medic.exe" -Uninstall /silent

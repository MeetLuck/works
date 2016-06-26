import subprocess
#subprocess.call(['df','-h'])
#subprocess.call('du -hs $HOME', shell=True)
p = subprocess.Popen(['echo','hello world'], stdout=subprocess.PIPE)
print p.communicate() # -> ('hello world\r\n', None)
#-------- return (stdoutdata,stderrdata)
import os
try:
    os.makedirs(r'H:\testaaa')
except WindowsError as e:
    print e

import os,time
myhome = os.path.expanduser('~')
myworks = os.path.join(myhome,'works')
myworks = os.path.abspath(myworks)
import subprocess
#os.system('cd /D D:',True)
subprocess.Popen('D:',shell=True)
#os.system('refreshenv')
#os.chdir('d:')
os.chdir(myworks)
cmd = 'cd %s' %myworks
#os.system('cd %s' %myworks)
print cmd,myworks

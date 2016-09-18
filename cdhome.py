import os,time
myhome = os.path.expanduser('~')
myworks = os.path.join(myhome,'works')
myworks = os.path.abspath(myworks)
os.system('D:')
os.chdir(myworks)
#os.system('cd %s' %myworks)
print os.curdir,myworks

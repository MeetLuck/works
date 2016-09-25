import os,sys
import subprocess
myhome = os.path.expanduser('~')
myworks = os.path.join(myhome,'works')
os.chdir(myworks)
confirm = raw_input('y or n \n')
if confirm = 'n':
    sys.exit()
#gitset = 'git remote set-url origin https://meetluck:pjw269505@github.com/meetluck/works.git'
#ps = subprocess.call(gitset, shell=True)
cmds = ['git init']
cmds.append('git config --local user.name meetluck') 
cmds.append('git config --local user.ename withpig1994@hanmail.net') 
cmds.append('git remote add origin https://github.com/MeetLuck/works.git')
for cmd in cmds:
    subprocess.call(cmd, shell=True)

import os,time
import subprocess
myhome = os.path.expanduser('~')
myworks = os.path.join(myhome,'works')
os.chdir(myworks)
worksdir = os.path.abspath(os.curdir)
assert os.path.basename(worksdir) == 'works', 'cwd is NOT home/works'

#gitset = 'git remote set-url origin https://meetluck:pjw269505@github.com/meetluck/works.git'
#ps = subprocess.call(gitset, shell=True)
ps = subprocess.call('git init', shell=True)
ps = subprocess.call('git pull origin master', shell=True)

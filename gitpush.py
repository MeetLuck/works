import os,time
myhome = os.path.expanduser('~')
myworks = os.path.join(myhome,'works')
os.chdir(myworks)
worksdir = os.path.abspath(os.curdir)
assert os.path.basename(worksdir) == 'works', 'cwd is NOT home/works'

lastmodified = time.strftime('%y%m%d') + time.strftime('-%H:%M')
print lastmodified
import subprocess
gitset = 'git remote set-url origin https://meetluck:pjw269505@github.com/meetluck/works.git'
ps = subprocess.call(gitset, shell=True)
ps = subprocess.call('git init', shell=True)
ps = subprocess.call('git add *', shell=True)
#ps = subprocess.call('git add -all', shell=True)
ps = subprocess.call('git status', shell=True)
ps = subprocess.call("git commit -m '%s'" % lastmodified, shell=True)
ps = subprocess.call('git push origin master', shell=True)

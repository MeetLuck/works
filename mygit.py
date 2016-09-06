import os,time
myhome = os.path.expanduser('~')
myworks = os.path.join(myhome,'works')
lastmodified = time.strftime('%y%m%d') + time.strftime('-%H:%M')
print lastmodified

os.chdir(myworks)
import subprocess
gitset = 'git remote set-url origin https://meetluck:pjw269505@github.com/meetluck/works.git'
ps = subprocess.call(gitset, shell=True)
ps = subprocess.call('git init', shell=True)
ps = subprocess.call('git add *', shell=True)
ps = subprocess.call('git status', shell=True)
ps = subprocess.call("git commit -m '%s'" % lastmodified, shell=True)
ps = subprocess.call('git push origin master', shell=True)

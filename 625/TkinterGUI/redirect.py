from Tkinter import *
from subprocess import Popen, PIPE, call, check_call
root = Tk()
text = Text(root)
text.pack()
#p = Popen( ['ls' ,'C:/windows','-l'], stdout = PIPE, bufsize =1, universal_newlines=True) 
#p = Popen( ['dir'], stdout = PIPE, bufsize =1, universal_newlines=True) 
#p = Popen('dir/w', shell=True,stdout=PIPE)
p = Popen(['dir/w'],shell=True ,stdout=PIPE)
#stdout, stderr = p.communicate()
#p = call(['dir','/W'])
#with Popen(['dir'], stdout = PIPE, bufsize=1, universal_newlines =True) as p:
#x = check_call(['dir','/W'],cwd='./')

#print x
for line in p.stdout:
    print line
    text.insert(END, line)
root.mainloop()

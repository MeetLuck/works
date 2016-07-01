import subprocess
proc = subprocess.Popen(['sleep','0.1'])
while proc.poll() is None:
    print 'Working...'
print 'Exit status', proc.poll()

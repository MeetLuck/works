import subprocess
# check_output( [executable, commandline arguments] )
lsout = subprocess.check_output(['ls','-l'])
print lsout
# ls command gets its first argument as '|' have not idea with '|'
# complain that no such file exists
try:
    lsout = subprocess.check_output(['ls','|','wc','-l'])
except:
    print "=> 'ls.exe' does not take pipe character as argument"
    print "=> use shell=True"
    print "=> subprocess.check_output('ls | wc -w', shell=True)"
#   lsout = subprocess.check_output('ls | wc -w',shell=True)
    lsout = subprocess.check_output(['ls','|','wc','-l'],shell=True)
    print lsout
#lsout = subprocess.check_output('dir | wc -l')
#print lsout

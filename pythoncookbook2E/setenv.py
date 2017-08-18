import sys, time ,math

key = sys.argv[1]
value = eval(' '.join(sys.argv[2:]) )
cmd = 'set %s=%s\n' %(key,value)
open('set_tmp.bat','w').write(cmd)


import os
import time,winsound
start = time.time()
eol = '\r\n'
def getlogfile():
    scriptdir = os.path.dirname( os.path.abspath(__file__) )
    filename = 'test.log'
    logfile = os.path.join(scriptdir,filename)
    return logfile

logfile = getlogfile()

print 'logfile:',logfile
if not os.path.exists(logfile): 
    testlog = open(logfile,'w')
    testlog.write('\n\n Created at %s\n' % time.ctime() )
    testlog.close()
testlog = open(logfile,'a')
testlog.write('\n\n Staring While loop at %s\n' % time.ctime() )
#winsound.Beep(100,50)
#winsound.Beep(150,100)
#winsound.Beep(200,150)
#winsound.Beep(250,200)
#winsound.Beep(300,350)
#winsound.Beep(350,250)
running = True
while running:
    elasped = time.time() - start
    if elasped > 5:
        #winsound.Beep(100,2650)
        #winsound.Beep(1000,2650)
        msg = "time's up : " + eol
        msg += 'started : %s\r\n' % time.ctime(start)
        msg += 'ended : %s\r\n'   % time.ctime()
        msg += str( int(elasped) )
        testlog.write(msg+'\r\n')
        print msg
        running= False
else:
    msg = os.path.abspath(__file__) + eol
    msg += os.__file__ + eol
    msg += os.path.__file__ + eol
    msg += str( int(elasped) ) + eol
    testlog.write(msg+'\r\n')
    print msg
    testlog.flush()
    testlog.close()

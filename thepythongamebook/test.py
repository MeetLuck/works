import time
start = time.time()
startctime = time.ctime()
count = 0
while True:
    if time.time() - start > 10.0:
        print startctime
        print time.ctime()
        print str(count//1.0e6) + ' M times'
        break
    count += 1

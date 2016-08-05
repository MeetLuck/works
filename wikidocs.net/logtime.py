import time
def logtime(func):
    ''' log elasped time '''
    def wrapper(*args):
        start = time.time()
        val = func(*args)
        elapsed = time.time() - start
        print '{} elasped'.format(elapsed)
        return val
    return wrapper

@logtime
def sumation(n):
    sum = 0
    for i in range(1,n+1):
        sum += i
    return sum

print sumation(1000)

def fib(n):
    if n==1 or n==0: return 1
    return fib(n-1) + fib(n-2)

fib1 = logtime(fib)
print fib1(33)

''' Coroutines 
    from http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python/231855#231855
'''
import os
cls = lambda : os.system('cls')

def bank_account(deposited, interest_rate):
    while True:
        interest = interest_rate * deposited
        received = yield interest
        if received:
            deposited += received
my_account = bank_account(1000, 0.05)
first_year_interest = my_account.next()
print first_year_interest
next_year_interest = my_account.send(first_year_interest + 1000)
print next_year_interest

cls()
def account(balance, interest_rate):
    print '-'*40
    print '  balance = {b}, interest_rate={r}'.format(b=balance,r=interest_rate)
    print '-'*40
    try:
        while True:
            interest = interest_rate * balance
            deposit = yield
            if deposit:
                print '>> deposited {d}'.format(d = deposit)
                interest += deposit * interest_rate
            balance += deposit + interest
            print ' my balance = {b},interest = {i}'.format(b=balance,i=interest)
    except GeneratorExit: pass

my_account = account(balance = 10000, interest_rate = 0.05); my_account.next()
my_account.send(1000)
my_account.send(1000)
my_account.send(10000)

cls()
def deposit_money(money,account):
    account.send(money)
def withraw_money(money,account):
    account.send(money)

def calcuate_account(balance,interest_rate,print_account):
    try:
        while True:
            deposit = (yield)
            balance += deposit
            interest = balance * interest_rate
            balance += interest
            account = (balance,deposit,interest)
            # send accout to print_account
            print_account.send(account)
    except GeneratorExit:
        print_account.close()

def  print_account():
    try:
        while True:
            account = yield
            balance,deposit,interest = account
            print '>> deposited {d}'.format(d = deposit)
            print ' old balance = {old}'.format(old = balance-(deposit+interest))
            print ' new balance = {b},interest = {i}'.format(b=balance,i=interest)
    except GeneratorExit:
        print '======== Done ========'

print_g = print_account(); print_g.next()
account = calcuate_account(10000,0.05,print_g) ; account.next()
deposit_money(1000,account)
deposit_money(1000,account)
deposit_money(10000,account)
withraw_money(-10000,account)
cls = cls()
cls
def fib(n,next_co):
    a, b = 0, 1
    try:
        for i in range(1,n+1):
    #        yield a
            a, b = b, a+b
            next_co.send((i,a))
    except GeneratorExit:
        next_co.close()

def printer():
    try:
        while True:
            i,a = yield
            print 'fib({i}) = {a}'.format(i=i,a=a)
    except GeneratorExit:
#       print 'fib({i}) = {a}'.format(i=i,a=a)
        print '====== Done printing ======='

p = printer();p.send(None)
f = fib(10,p)


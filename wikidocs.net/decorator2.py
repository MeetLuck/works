def factorial(n):
    if n == 1: return 1
    return n * factorial(n-1)

def decorator(func):
    func.indent = 0
    def wrapper(n):
        print '{}-> call {}({})'.format('  ' * func.indent,func.__name__, n) 
        func.indent += +1
        val = func(n)
        func.indent += -1
        print '{}<- return {}({}) = {}'.format('  ' * func.indent, func.__name__, n,val)
        return val
    return wrapper

factorial = decorator(factorial)
factorial(5)

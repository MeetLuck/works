def arg_decorator(scale=1):
    def decorator(func):
        def wrapper(*args):
            print 'scale = {}'.format(scale)
            val = scale * func(*args) 
            return val
        return wrapper
    return decorator

@arg_decorator(scale=100)
def plus(x,y):
    return x+y

@arg_decorator(scale=0.01)
def minus(x,y):
    return x-y

print plus(1,2)
print minus(1,2)

from functools import wraps
def decorator(func):
    @wraps(func)
    def wrapper(*args):
        ''' wrapper docstring ... '''
        val = func(*args)
        return val
#   wrapper.__doc__ = func.__doc__
#   wrapper.__name__ = func.__name__
    return wrapper

def original(n):
    ''' original docstring ... '''
    pass

print original
# <function original at 0x02E33XXX>
original = decorator(original)
print original
# <function original at 0x02E33YYY>
# same name but different address
print original(3)
print original.__doc__
print help(original)

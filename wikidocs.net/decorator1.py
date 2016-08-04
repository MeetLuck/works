def original(x,recursive = [-1]):
    recursive[0] += 1
    if recursive[0] > 3: return
    print '-> original call {}({}) \trecursive depth = {}'.format(original.__name__,x, recursive[0] )
    original(x)

def decorator(func):
    def wrapper(x):
        print '... wrapper calls {}({})'.format(func.__name__,x)
        output = func(x)
        return output
    return wrapper

# <function original at 0x02018BF0> exists in global environment
original = decorator(original)
" she's gone!!! "
# at this point, original points to <function wrapper at 0x...> 
# so that <function original> does not exist in global environment, it's gone!!!
# we can not directly call <function original at 0x...> any more.
# but it is kept in <function wrapper at 0x...>'s secret place called func_closure.
original(3)
# calling <function wrapper at 0x...>( (2,) )

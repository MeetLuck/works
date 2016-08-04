def original(*args): pass

def decorator(func):
    def wrapper(*args):
        print 'calling {}({})'.format(wrapper,args)
        output = func(*args)
        return output
    return wrapper

# <function original at 0x02018BF0> exists in global environment
original = decorator(original)
" she's gone!!! "
# at this point, original points to <function wrapper at 0x...> 
# so that <function original> does not exist in global environment, it's gone!!!
# we can not directly call <function original at 0x...> any more.
# but it is kept in <function wrapper at 0x...>'s secret place called func_closure.
print original.func_code.co_varnames
print original.func_closure[0].cell_contents
original(2)
# calling <function wrapper at 0x...>( (2,) )

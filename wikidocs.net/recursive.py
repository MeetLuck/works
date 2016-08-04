def factorial(n,recursive = [0]):
    print '-> call\t  {}({})\t\trecursion depth = {}'.format(factorial.func_name,n, recursive[0] )
    recursive[0] += +1
    if n != 1: 
        val =  n * factorial(n-1)
    else:
        val = 1
    recursive[0] += -1
    print '<- return {}({}) = {}\trecursion depth = {}'.format(factorial.func_name,n, val,recursive[0] )
    return val

print factorial(5)

def fact(n,recursive = [0]):
    print '{} -> call  fact({})'.format( ' ' * 2 *recursive[0], n  )
    recursive[0] += +1
    if n != 1: 
        val =  n * fact(n-1)
    else:
        val = 1
    recursive[0] += -1
    print '{} <- return fact({}) = {}'.format( ' ' * 2 *recursive[0], n, val  )
    return val

print fact(5)


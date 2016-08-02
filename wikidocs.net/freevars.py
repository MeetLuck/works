def outer():
    free = -99
    def inner():
        global free
        free  = free + 1
        print free
        print inner.func_code.co_freevars
    return inner
    

f = outer()
f()
    



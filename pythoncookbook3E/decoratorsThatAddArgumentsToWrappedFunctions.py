# 9.11 Writing Decorators that Add Arguments to Wrapped Functions
# python version 3 required

def optional_debug(func):
    def wrapper(*args,debug=False,**kwargs):
        print( args,debug,kwargs )
        if debug:
            print( 'calling', func.__name__ )
        return func(*args,**kwargs)
    return wrapper

def test():
    @optional_debug
    def spam(a,b,c):
        print( a,b,c )

    spam(1,2,3)
    spam(1,2,3,debug=True)

if __name__ == '__main__':
    test()

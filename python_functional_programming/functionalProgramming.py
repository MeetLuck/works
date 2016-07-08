''' 13. Functional Programming'''

#------- 13.1 Functions as objects -----------------
def i_am_an_object(myarg):
    ''' I am a really nice function '''
    return myarg
print i_am_an_object(10)
an_object_by_any_other_name = i_am_an_object
print an_object_by_any_other_name(20)
print repr(i_am_an_object)
print repr(an_object_by_any_other_name)
print i_am_an_object.__doc__
#----- 13.2 Higher-order Functions ------------------
# means that functions can accept other functions as arguments and
# returns functions to the caller
print i_am_an_object(i_am_an_object)
#----- 13.3 Sorting:An Example of Higher-Order functions  ---------
def second_element(t):
    return t[1]
zepp = [('Guitar','Jimmy'), ('Vocals','Robert'),('Bass','John Paul') ]
print sorted(zepp)
print sorted(zepp, key=second_element)
#----- 13.4 Anonymouse Functions ----------------------
import operator
def call_func(f, *args):
    print f.__name__
    return f(*args)
print call_func(lambda x,y: x + y,    4,5 )
print call_func(operator.add, 4,5)
#----- 13.5 Nested functions ----------------------
def outer():
    def inner(a):
        return a
    return inner
f = outer()
print f, f.__name__
print f(10)
#----- 13.6 Closures ----------------------
'''
    A nested function has access to the environment in which it was defined.
    The defintion occurs during the execution of the outer function.
    Therefore, it is possible to return an inner function that remembers the
    state of the outer function, even after the outer function has completed
    execution. '''
def outer2(a):
    def inner2(b):
        return a + b
    return inner2
add1 = outer2(10)
print add1
print add1(20)
#--------- Lexical Scoping --------------------------
def outer():
    count = 0
    def inner():
        count += 1
        return count
    return inner
counter = outer()
#print counter() # UnboundLocalError: local variable 'count' referenced before assignment

def better_outer():
    count = [0]
    def inner():
        count[0] += 1
        return count[0]
    return inner
counter = better_outer()
print counter()
print counter()
print counter()
#------ 13.8 Useful function object: operator -------------
get_second = operator.itemgetter(1)
print get_second( ['a','b','c','d'] )
# itemgetter function returns a tuple if it is given more than one index
get_02 = operator.itemgetter(0,2)
print get_02( ['a','b','c','d'] )
# A typical use for the itemgetter() function is as the key argument to a list sort
print sorted(zepp, key=operator.itemgetter(1) )

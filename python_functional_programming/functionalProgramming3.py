#------- 13.10 Decorators ----------------------------
def simple(*args):
    for arg in args:
        print arg,
    print
simple('a','b','c')

def logit(func):
    def wrapper(*args, **kwargs):
        print 'function <%s> called with args %s' %(func.__name__, args)
        func(*args, **kwargs)
    return wrapper
logged_simple = logit(simple)
logged_simple('a','b','c')

#----------- functional-1-langs.py
import itertools

CLAIM = '{0} is the # {1} {2} language'

def best(type, *args):
    langs = list() 
    for i, arg in enumerate(args):
        langs.append(CLAIM.format(arg, i+1, type) )
    return langs
def best_functional(*args):
    return best('functional', *args)
def best_OO(*args):
    return best('OO', *args)
def python_rules(func):
    def wrapper(*args, **kwargs):
        new_args = ['Python']
        new_args.extend(args)
        return func(*new_args)
    return wrapper
best_OO = python_rules(best_OO)
for claim in itertools.chain( best_functional('Haskell', 'Erlang'), [''],
        best_OO('Objective-C','Java') ):
    print claim

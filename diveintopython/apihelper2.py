def info2(object, spacing=10, collapse=1):
    ''' Print methods and doc strings '''
    methodList = list()
    for method in dir(object):
        if callable( getattr(object, method) ) and not method.startswith('__'):
            methodList.append(method)
#   methodList = [ method for method in dir(object) if callable( getattr(object, method) ) ]
    if collapse:
        processFunc = lambda s: ' '.join(s.split())
    else:
        processFunc = lambda s: s
    for method in methodList:
        m,p =  method.ljust(spacing) , processFunc( str(getattr(object,method).__doc__) )
        print '%s %s' %(m,p)

if __name__ == '__main__':
#   li = list()
#   info2(li)
#   info2(dict())
    from UserDict import UserDict
    info2(UserDict)

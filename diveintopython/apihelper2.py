def info2(object, spacing=10, collapse=1):
    ''' Print methods and doc strings '''
    methodList = [ method for method in dir(object) if callable( getattr(object, method) ) ]
    if collapse:
        processFunc = lambda s: ' '.join(s.split())
    else:
        processFunc = lambda s: s
    for method in methodList:
        m,p =  method.ljust(spacing) , processFunc( str(getattr(

''' chapter 4.  The Power Of Introspection '''
#-------- Example 4.1 apihelper.py -------------------
def info(object, spacing=20, collapse=1):
    ''' Print methods and doc strings.
    Takes module, class, list, dictionary, or string '''

    methodList = [ method for method in dir(object) if callable( getattr(object,method) ) ]
    processFunc = collapse and (lambda s: ' '.join( s.split() ) )   or (lambda s: s )
    print '\n'.join( ['%s %s' %(method.ljust(spacing),
                                processFunc( str(getattr(object,method).__doc__) ) )
                                for method in methodList ] )
if __name__ == '__main__':
    li = list()
    string = str()
    info(string)
    print '\n\n'
    info(li)


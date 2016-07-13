''' Miscellaneous utility functions '''
def openAnything(source):
    ''' URI, filename, or string --> stream
    This function lets you define parsers that take any input source
    (URI, pathname to local or network file, or actual data as a string)
    and deal with it in a uniform manner.
    Returned object is guaranteed to have all the basic stdio read methods
    Just .close() the object when you're done with it.
    Examples:
    >>> from xml.dom import minidom
    >>> sock = openAnything('http://localhost/kant.html')
    >>> doc = minidom.parse(sock)
    >>> sock.close()
    >>> sock = openAnything("c:\\inetpub\\wwwroot\\kant.xml")
    >>> doc = minidom.parse(sock)
    >>> sock.close()
    >>> sock = openAnything("<ref id='conjunction'><text>and</text><text>or</text></ref>")
    >>> doc = minidom.parse(sock)
    >>> sock.close()
    '''
    if hasattr(source,'read'):
        return source
    if source == '-':
        import sys
        return sys.stdin
    # try to open with urllib if source is http, ftp, or file URL
    import urllib
    try:
        return urllib.urlopen(source)
    except (IOError, OSError):
        pass
    # try to open with native open function if source is pathname
    try:
        return open(source)
    except (IOError, OSError):
        pass
    # treat source as string
    import StringIO
    return StringIO.StringIO( str(source) )



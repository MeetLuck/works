import htmlentitydefs
from sgmllib import SGMLParser

class BaseHTMLProcessor2(SGMLParser):
    def reset(self):
        ' extend called by SGMLParser.__init__ '
        self.pieces = list()
        SGMLParser.reset(self)
    def unknown_starttag(self, tag, attrs):
        stratts = ''.join( [' %s="%s" ' %(k,v) for k,v in attrs] )
        self.pieces.append("<%(tag)s%(strattrs)s>" % locals() )


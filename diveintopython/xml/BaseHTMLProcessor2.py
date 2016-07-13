import htmlentitydefs
from sgmllib import SGMLParser

class BaseHTMLProcessor2(SGMLParser):
    def reset(self):
        ' extend called by SGMLParser.__init__ '
        self.pieces = list()
        SGMLParser.reset(self)
    def unknown_starttag(self, tag, attrs):
        ''' 
        >>> tag = a
        >>> attr = [ ('href', 'index.html'), ('title','Go to home page') ]
         <a href="index.html" title="Go to home page">
        '''
        strattrs = ''.join( [' %s="%s" ' %(k,v) for k,v in attrs] )
        self.pieces.append("<%(tag)s%(strattrs)s>" % locals() )

        print '*'*80
        print 'called unknown_starttag:  %s' %tag
        print ''.join(self.pieces)
        print '*'*80
    def unknown_endtag(self, tag):
        # </div>
        self.pieces.append("</%(tag)s>" % locals() )
    def handle_charref(self, ref):
        ''' numeric character reference
        >>> &#entity_number &#160; <=> &nbsp;
        '''
        self.pieces.append("&#%(ref)s;" % locals() )
    def handle_entityref(self, ref):
        ''' entity reference
        >>> &entity_name;
        >>> '<'  == '&lt;' or '&#60;'
        '''
        self.pieces.append("&%(ref)s" % locals() )
        if htmlentitydefs.entitydefs.has_key(ref):
            self.pieces.append(";")
    def handle_data(self,text):
        self.pieces.append(text)

        print '*'*80
        print 'called handle_data:  %s' %text
        print ''.join(self.pieces)
        print '*'*80
    def handle_comment(self,text):
        self.pieces.append("<!--%(text)s-->" %locals() )
    def handle_pi(self, text):
        self.pieces.append("<?%(text)s>" % locals() )
    def handle_decl(self,text):
        # HTML Declaration like <!DOCTYPE html ... >
        self.pieces.append("<!%(text)s>" % locals() )
    def output(self):
        ''' Returned processed HTML as a single string '''
        return ''.join(self.pieces)

if __name__ =='__main__':
    htmlSource = '''
    <title> Test Page </title>
    '''
    parser = BaseHTMLProcessor2()
    parser.feed(htmlSource)
    print parser.output()



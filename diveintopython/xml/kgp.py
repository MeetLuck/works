''' Kant Generator for python
 Generates mock philosophy based on a context-free grammar
 Usage: python kgp.py [options] [source]
 Options:
    -g ..., --grammar=... use specified grammar file or URL
    -h, --help            show this hlep
    -d                    show debugging information while parsing

 Examples:
    kgp.py                  generates several paragraphs of Kantian philosophy
    kgp.py -g husserl.xml   generates several paragraphs of Husserl
    kgp.py "<xref id='paragraph'/>" generates a paragraph of Kant
    kgp.py template.xml     reads from template.xml to decide what to generate
'''
from xml.dom import minidom
import random
import toolbox
import sys
import getopt

_debug = 0

class NoSourceError(Exception): pass

class KantGenerator:
    ''' generates mock philosopy based on a context-free grammar'''
    def __init__(self, grammar, source=None):
        self.loadGrammar(grammar)
        self.loadSource(source and source or self.getDefaultSource() )
        self.refresh()
    def _load(self, source):
        '''load XML input source, return parsed XML document
        - a URL of remote XML file ('http://divintopython.org/kant.xml')
        - a filename of a local XML file('~/divintopytho/py/kant.xml')
        - standard input('-')
        - the actual XML document, as a string
        '''
        sock = toolbox.openAnything(source)
        xmldoc = minidom.parse(sock).documentElement
        sock.close()
        return xmldoc
    def loadGrammar(self, grammar):
        ''' load context-free grammar'''
        self.grammar = self._load(grammar)
        self.refs = dict() 
        for ref in self.grammar.getElementsByTagName('ref'):
            self.refs[ref.attributes['id'].value] = ref
    def loadSource(self, source):
        self.source = self._load(source)
    def getDefaultSource(self):
        ''' guess default source of the current grammar
        The default source will be one of the <ref>s that is not
        cross-referenced. 
        Example: The default source for kant.xml is "<xref id='section'/>",
        because 'section' is the one <ref> that is not <xref>'d anywhere in
        the grammar. In most grammars, the default source will produce the
        loggest(and most interesting) output.
        '''
        xrefs = dict()
        for xref in self.grammar.getElementsByTagName('xref'):
            xrefs[xref.attributes['id'].value] = 1
        xrefs = xrefs.keys()
        standaloneXrefs = [e for e in self.refs.keys() if e not in xrefs]
        if not standaloneXrefs:
            raise NoSourceError, "can't guess source, and no source specified"
        return '<xref id="%s"/>' % random.choice(standaloneXrefs)
    def reset(self):
        ''' reset parser '''
        self.pieces = []
        self.capitalizeNextWord = 0
    def refresh(self):
        ''' reset output buffer, re-parse entire source file, and return output
        Since parsing involves a good deal of randomness, this is an easy way to
        get new output without having to reload a grammar file each time
        '''
        self.reset()
        self.parse(self.source)
        return self.output()
    def output(self):
        return ''.join(self.pieces)
    def randomChildElement(self,node):
        ''' choose a random child element of a node
        This is a utility method used by do_xref and do_choice
        '''
        choices = [ e for e in node.childNodes if e.nodeType == e.ELEMENT_NODE]
        chosen = random.choice(choices)
        if _debug:
            sys.stderr.write('%s available choices: %s\n' %( len(choices),[e.toxml() for e in choices] ) )
            sys.stderr.write('Chosen: %s\n' % chosen.toxml() )
        return chosen
    def parse(self,node):
        ''' parse a single XML node
        A parsed XML document from minidom.parse is a tree of nodes of various types.
        Each node is represented by an instance of the corresponding python class
        (Element for a tag, Text for  text data, Document for the top-level document)
        The following statement constructs the name of a class method based on the type
        of node we're parsing and then calls the method
        '''
        parseMethod = getattr(self, 'parse_%s' % node.__class__.__name__)
        parseMethod(node)
    def parse_Document(self,node):
        ''' parse the document node
        The document node by itself isn't interesting, but its only child, node.documentElement,
        is the root node of the grammar.
        '''
        self.parse(node.documentElement)
    def parse_Text(self,node):
        text = node.data
        if self.capitalizeNextWord:
            self.pieces.append( text[0].upper() )
            self.pieces.append( text[1:])
            self.capitalizeNextWord = 0
        else:
            self.pieces.append(text)
    def parse_Element(self,node):
        handlerMethod = getattr(self,'do_%s' % node.tagName)
        handlerMethod(node)
    def parse_Comment(self,node):
        pass
    def do_xref(self,node):
        id = node.attributes['id'].value
        self.parse( self.randomChildElement(self.refs[id]) )
    def do_p(self, node):
        keys = node.attributes.keys()
        if 'class' in keys:
            if node.attributes['class'].value == 'sentence':
                self.capitalizeNextWord = 1
        if 'chance' in keys:
            chance = int( node.attributes['chance'].value)
            doit = ( chance > random.randrange(100) )  
        else:
            doit = 1
        if doit:
            for child in node.childNodes: self.parse(child)
    def do_choice(self, node):
        self.parse( self.randomChildElement(node) )
    def usage():
        print __doc__

def main(argv):
    grammar = 'kant.xml'
    try:
        opts, args = getopt.getopt(argv, 'hg:d', ['help', 'grammar='] )
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h','--help'):
            usage()
            sys.exit()
        elif opt == '-d':
            global _debug
            _debug = 1
        elif opt in ('-g','--grammar'):
            grammar = arg
    source = ''.join(args)
    k = KantGenerator(grammar, source)
    print k.output()
if __name__ == '__main__':
    main(sys.argv[1:])

                              

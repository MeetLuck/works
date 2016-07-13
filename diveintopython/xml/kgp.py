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
        for ref in self.grammar.getElementByTagName('ref'):
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
        self.
